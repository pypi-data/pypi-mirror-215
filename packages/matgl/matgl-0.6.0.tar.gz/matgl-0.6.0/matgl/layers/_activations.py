"""Custom activation functions."""
from __future__ import annotations

import math

import torch
from torch import nn


class SoftPlus2(nn.Module):
    """SoftPlus2 activation function:
    out = log(exp(x)+1) - log(2)
    softplus function that is 0 at x=0, the implementation aims at avoiding overflow.
    """

    def __init__(self) -> None:
        """Initializes the SoftPlus2 class."""
        super().__init__()
        self.ssp = nn.Softplus()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Evaluate activation function given the input tensor x.

        Args:
            x (torch.tensor): Input tensor

        Returns:
            out (torch.tensor): Output tensor
        """
        return self.ssp(x) - math.log(2.0)


class SoftExponential(nn.Module):
    """Soft exponential activation.
    When x < 0, SoftExponential(x,alpha) = -log(1-alpha(x+alpha))/alpha
    When x = 0, SoftExponential(x,alpha) = 0
    When x > 0, SoftExponential(x,alpha) = (exp(alpha*x)-1)/alpha + alpha.

    References: https://arxiv.org/pdf/1602.01321.pdf
    """

    def __init__(self, alpha: float = None):
        """
        Init SoftExponential with alpha value.

        Args:
            alpha (float): adjustable Torch parameter during the training.
        """
        super().__init__()

        # initialize alpha
        if alpha is None:
            self.alpha = nn.Parameter(torch.tensor(0.0))
        else:
            self.alpha = nn.Parameter(torch.tensor(alpha))

        self.alpha.requires_grad_(True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Evaluate activation function given the input tensor x.

        Args:
            x (torch.tensor): Input tensor

        Returns:
            out (torch.tensor): Output tensor
        """
        if self.alpha == 0.0:
            return x
        if self.alpha < 0.0:
            return -torch.log(1.0 - self.alpha * (x + self.alpha)) / self.alpha
        return (torch.exp(self.alpha * x) - 1.0) / self.alpha + self.alpha
