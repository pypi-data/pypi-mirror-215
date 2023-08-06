import torch
import torch.nn as nn
import torch.nn.functional as F

from torch import Tensor

from torch_activation.utils import plot_activation


class GCU(nn.Module):
    r"""
    Applies the Growing Cosine Unit activation function:

    :math:`\text{GCU}(x) = x \cos (x)`

    Args:
        inplace (bool, optional): can optionally do the operation in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.
        
    Examples::

        >>> m = nn.GCU()
        >>> x = torch.randn(2)
        >>> output = m(x)

        >>> m = nn.GCU(inplace=True)
        >>> x = torch.randn(2)
        >>> m(x)
    """

    def __init__(self, inplace: bool = False):
        super(GCU, self).__init__()
        self.inplace = inplace

    def forward(self, x) -> Tensor:
        if self.inplace:
            return x.mul_(torch.cos(x))
        else:
            return x * torch.cos(x)


class CosLU(nn.Module):
    r"""
    Applies the Cosine Linear Unit function:

    :math:`\text{CosLU}(x) = (x + \alpha \cdot \cos(\beta x)) \cdot \sigma(x)`

    Args:
        alpha (float, optional): Scaling factor for the cosine term. Default is 1.0.
        beta (float, optional): Frequency factor for the cosine term. Default is 1.0.
        inplace (bool, optional): can optionally do the operation in-place. Default: ``False``

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.

    Examples::

        >>> m = CosLU(alpha=2.0, beta=1.0)
        >>> x = torch.randn(2)
        >>> output = m(x)

        >>> m = CosLU(inplace=True)
        >>> x = torch.randn(2, 3, 4)
        >>> m(x) 
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0, 
                 inplace: bool = False):
        super(CosLU, self).__init__()
        self.alpha = nn.Parameter(torch.tensor(alpha))
        self.beta = nn.Parameter(torch.tensor(beta))
        self.inplace = inplace

    def forward(self, x) -> Tensor:
        return self._forward_inplace(x) if self.inplace else self._forward(x)

    def _forward(self, x):
        result = x + self.alpha * torch.cos(self.beta * x)
        result *= torch.sigmoid(x)
        return result

    def _forward_inplace(self, x):
        s_x = torch.sigmoid(x)
        x.add_(self.alpha * torch.cos(self.beta * x))
        x.mul_(s_x)
        del s_x
        return x


class SinLU(nn.Module):
    r"""
    Applies the Sinu-sigmoidal Linear Unit activation function:

    :math:`\text{SinLU}(x) = (x + \alpha \sin (\beta x)) \sigma (x)`

    Args:
        a (float, optional): Initial value for sine function magnitude. Default: 1.0.
        b (float, optional): Initial value for sine function period. Default: 1.0.

    Shape:
        - Input: :math:`(*)`, where :math:`*` means any number of dimensions.
        - Output: :math:`(*)`, same shape as the input.

    Examples::

        >>> m = nn.SinLU(a=5.0, b=6.0)
        >>> x = torch.randn(2)
        >>> output = m(x)
    """
    def __init__(self, a: float = 1.0, b: float = 1.0):
        super(SinLU, self).__init__()
        self.a = nn.Parameter(torch.Tensor([a]))
        self.b = nn.Parameter(torch.Tensor([b]))

    def forward(self, x) -> Tensor:
        return (x + self.a * torch.sin(self.b * x)) * torch.sigmoid(x)
