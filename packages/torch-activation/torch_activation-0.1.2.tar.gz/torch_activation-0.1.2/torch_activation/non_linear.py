import torch
import torch.nn as nn
import torch.nn.functional as F

from torch import Tensor


class CoLU(nn.Module):
    r"""
    Applies the Collapsing Linear Unit activation function:

    :math:`\text{CoLU}(x) = \frac{x}{1-x \cdot e^{-(x + e^x)}}`

    Args:
        inplace (bool, optional): can optionally do the operation in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.

    Examples::

        >>> m = nn.CoLU()
        >>> x = torch.randn(2)
        >>> output = m(x)

        >>> m = nn.CoLU(inplace=True)
        >>> x = torch.randn(2)
        >>> m(x)
    """

    def __init__(self, inplace=False):
        super(CoLU, self).__init__()
        self.inplace = inplace

    def forward(self, x) -> Tensor:
        if self.inplace:
            return x.div_(1 - x * torch.exp(-1 * (x + torch.exp(x))))
        else:
            return x / (1 - x * torch.exp(-1 * (x + torch.exp(x))))


class ScaledSoftSign(torch.nn.Module):
    r"""
    Applies the ScaledSoftSign activation function:

    :math:`\text{ScaledSoftSign}(x) = \frac{\alpha \cdot x}{\beta + \|x\|}`

    Args:
        alpha (float, optional): The initial value of the alpha parameter.
        beta (float, optional): The initial value of the beta parameter.

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.

    Examples:
        >>> m = ScaledSoftSign(alpha=0.5, beta=1.0)
        >>> x = torch.randn(2, 3)
        >>> output = m(x)

        >>> m = ScaledSoftSign(inplace=True)
        >>> x = torch.randn(2, 3)
        >>> m(x)
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0):
        
        super(ScaledSoftSign, self).__init__()

        self.alpha = torch.nn.Parameter(torch.tensor(alpha))
        self.beta = torch.nn.Parameter(torch.tensor(beta))

    def forward(self, x) -> Tensor:
        abs_x = x.abs()
        alpha_x = self.alpha * x
        denom = self.beta + abs_x
        result = alpha_x / denom
        return result


if __name__ == "__main__":
    pass
