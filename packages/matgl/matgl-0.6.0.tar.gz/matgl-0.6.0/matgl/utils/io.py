"""Provides utilities for managing models and data."""
from __future__ import annotations

import inspect
import json
import logging
import os
import warnings
from pathlib import Path

import requests
import torch

from matgl.config import MATGL_CACHE, PRETRAINED_MODELS_BASE_URL

logger = logging.getLogger(__file__)


class IOMixIn:
    """Mixin class for model saving and loading.

    For proper usage, models should subclass nn.Module and IOMix and the `save_args` method should be called
    immediately after the `super().__init__()` call::

        super().__init__()
        self.save_args(locals(), kwargs)

    """

    def save_args(self, locals: dict, kwargs: dict | None = None) -> None:
        r"""Method to save args into a private _init_args variable.

        This should be called after super in the __init__ method, e.g., `self.save_args(locals(), kwargs)`.

        Args:
            locals: The result of locals().
            kwargs: kwargs passed to the class.
        """
        args = inspect.getfullargspec(self.__class__.__init__).args
        d = {k: v for k, v in locals.items() if k in args and k not in ("self", "__class__")}
        if kwargs is not None:
            d.update(kwargs)

        # If one of the args is a subclass of IOMixIn, we will serialize that class.
        for k, v in d.items():
            if issubclass(v.__class__, IOMixIn):
                d[k] = {
                    "@class": v.__class__.__name__,
                    "@module": v.__class__.__module__,
                    "@model_version": getattr(v, "__version__", 0),
                    "init_args": v._init_args,
                }
        self._init_args = d

    def save(self, path: str | Path = ".", metadata: dict | None = None, makedirs: bool = True):
        """Save model to a directory.

        Three files will be saved.
        - path/model.pt, which contains the torch serialized model args.
        - path/state.pt, which contains the saved state_dict from the model.
        - path/model.json, a txt version of model.pt that is purely meant for ease of reference.

        Args:
            path: String or Path object to directory for model saving. Defaults to current working directory (".").
            metadata: Any additional metadata to be saved into the model.json file. For example, a good use would be
                a description of model purpose, the training set used, etc.
            makedirs: Whether to create the directory using os.makedirs(exist_ok=True). Note that if the directory
                already exists, makedirs will not do anything.
        """
        path = Path(path)
        if makedirs:
            os.makedirs(path, exist_ok=True)

        torch.save(self._init_args, path / "model.pt")  # type: ignore
        torch.save(self.state_dict(), path / "state.pt")  # type: ignore
        d = {
            "@class": self.__class__.__name__,
            "@module": self.__class__.__module__,
            "@model_version": getattr(self, "__version__", 0),
            "metadata": metadata,
            "kwargs": self._init_args,
        }  # type: ignore
        with open(path / "model.json", "w") as f:
            json.dump(d, f, default=lambda o: str(o), indent=4)

    @classmethod
    def load(cls, path: str | Path | dict, **kwargs):
        """Load the model weights from a directory.

        Args:
            path (str|path|dict): Path to saved model or name of pre-trained model. If it is a dict, it is assumed to
                be of the form::

                    {
                        "model.pt": path to model.pt file,
                        "state.pt": path to state file,
                        "model.json": path to model.json file
                    }

                Otherwise, the search order is path, followed by download from PRETRAINED_MODELS_BASE_URL
                (with caching).
            **kwargs: Additional kwargs passed to RemoteFile class. E.g., a useful one might be force_download if you
                want to update the model.

        Returns: model_object.
        """
        fpaths = path if isinstance(path, dict) else _get_file_paths(Path(path), **kwargs)

        with open(fpaths["model.json"]) as f:
            model_data = json.load(f)

        _check_ver(cls, model_data)

        if not torch.cuda.is_available():
            state = torch.load(fpaths["state.pt"], map_location=torch.device("cpu"))
        else:
            state = torch.load(fpaths["state.pt"])
        d = torch.load(fpaths["model.pt"])

        # Deserialize any args that are IOMixIn subclasses.
        for k, v in d.items():
            if isinstance(v, dict) and "@class" in v and "@module" in v:
                modname = v["@module"]
                classname = v["@class"]
                mod = __import__(modname, globals(), locals(), [classname], 0)
                cls_ = getattr(mod, classname)
                _check_ver(cls_, v)  # Check version of any subclasses too.
                d[k] = cls_(**v["init_args"])
        d = {k: v for k, v in d.items() if not k.startswith("@")}
        model = cls(**d)
        model.load_state_dict(state)  # type: ignore

        return model


class RemoteFile:
    """Handling of download of remote files to a local cache."""

    def __init__(self, uri: str, cache_location: str | Path = MATGL_CACHE, force_download: bool = False):
        """Args:
        uri: Uniform resource identifier.
        cache_location: Directory to cache downloaded RemoteFile. By default, downloaded models are saved at
        $HOME/.matgl.
        force_download: To speed up access, a model with the same name in the cache location will be used if
        present. If you want to force a re-download, set this to True.
        """
        self.uri = uri
        toks = uri.split("/")
        self.model_name = toks[-2]
        self.fname = toks[-1]
        cache_location = Path(cache_location)
        os.makedirs(cache_location / self.model_name, exist_ok=True)
        self.local_path = cache_location / self.model_name / self.fname
        if (not self.local_path.exists()) or force_download:
            logger.info("Downloading from remote location...")
            self._download()
        else:
            logger.info(f"Using cached local file at {self.local_path}...")

    def _download(self):
        r = requests.get(self.uri, allow_redirects=True)
        with open(self.local_path, "wb") as f:
            f.write(r.content)

    def __enter__(self):
        """Support with context.

        Returns:
            Stream on local path.
        """
        self.stream = open(self.local_path, "rb")  # noqa: SIM115
        return self.stream

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the with context.

        Args:
            exc_type: Usual meaning in __exit__.
            exc_val: Usual meaning in __exit__.
            exc_tb: Usual meaning in __exit__.
        """
        self.stream.close()


def load_model(path: Path, **kwargs):
    r"""Convenience method to load a model from a directory or name.

    Args:
        path (str|path): Path to saved model or name of pre-trained model. The search order is path, followed by
            download from PRETRAINED_MODELS_BASE_URL (with caching).
        **kwargs: Additional kwargs passed to RemoteFile class. E.g., a useful one might be force_download if you
            want to update the model.

    Returns:
        Returns: model_object if include_json is false. (model_object, dict) if include_json is True.
    """
    path = Path(path)

    fpaths = _get_file_paths(path, **kwargs)

    try:
        with open(fpaths["model.json"]) as f:
            d = json.load(f)
            modname = d["@module"]
            classname = d["@class"]

            mod = __import__(modname, globals(), locals(), [classname], 0)
            cls_ = getattr(mod, classname)
            return cls_.load(fpaths, **kwargs)
    except BaseException:
        raise ValueError(
            "Bad serialized model detected. It is possible that you have an older model cached. Please "
            'clear your cache by running `python -c "import matgl; matgl.clear_cache()"`'
        ) from None


def _get_file_paths(path: Path, **kwargs):
    """Search path for files.

    Args:
        path (Path): Path to saved model or name of pre-trained model. The search order is path, followed by
            download from PRETRAINED_MODELS_BASE_URL (with caching).
        **kwargs: Additional kwargs passed to RemoteFile class. E.g., a useful one might be force_download if you
            want to update the model.

    Returns:
        {
            "model.pt": path to model.pt file,
            "state.pt": path to state file,
            "model.json": path to model.json file
        }
    """
    fnames = ("model.pt", "state.pt", "model.json")

    if all((path / fn).exists() for fn in fnames):
        return {fn: path / fn for fn in fnames}

    try:
        return {fn: RemoteFile(f"{PRETRAINED_MODELS_BASE_URL}{path}/{fn}", **kwargs).local_path for fn in fnames}
    except BaseException:
        raise ValueError(
            f"No valid model found in {path} or among pre-trained_models at "
            f"{MATGL_CACHE} or {PRETRAINED_MODELS_BASE_URL}."
        ) from None


def _check_ver(cls_, d: dict):
    """Check version of cls_ in current matgl against those noted in a model.json dict.

    Args:
        cls_: Class object.
        d: Dict from serialized json.

    Raises:
        Deprecation warning if the code is
    """
    if getattr(cls_, "__version__", 0) > d.get("@model_version", 0):
        warnings.warn(
            "Incompatible model version detected! The code will continue to load the model but it is "
            "recommended that you provide a path to an updated model, increment your @model_version in model.json "
            "if you are confident that the changes are not problematic, or clear your ~/.matgl cache using "
            '`python -c "import matgl; matgl.clear_cache()"`',
            UserWarning,
            stacklevel=2,
        )


def get_available_pretrained_models() -> list[str]:
    """Checks Github for available pretrained_models for download. These can be used with load_model.

    Returns:
        List of available models.
    """
    r = requests.get("https://api.github.com/repos/materialsvirtuallab/matgl/contents/pretrained_models")
    return [d["name"] for d in json.loads(r.content.decode("utf-8")) if d["type"] == "dir"]
