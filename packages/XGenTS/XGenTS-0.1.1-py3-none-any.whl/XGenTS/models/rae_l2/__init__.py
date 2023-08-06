"""This module is the implementation of the Regularized AE with L2 decoder parameter regularization
proposed in (https://arxiv.org/abs/1903.12436).

Available samplers
-------------------

.. autosummary::
    ~XGen.samplers.NormalSampler
    ~XGen.samplers.GaussianMixtureSampler
    ~XGen.samplers.MAFSampler
    ~XGen.samplers.IAFSampler
    :nosignatures:
"""

from .rae_l2_config import RAE_L2_Config
from .rae_l2_model import RAE_L2

__all__ = ["RAE_L2", "RAE_L2_Config"]
