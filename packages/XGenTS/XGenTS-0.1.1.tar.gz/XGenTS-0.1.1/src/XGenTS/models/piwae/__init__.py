"""This module is the implementation of the Partially Importance Weighted Autoencoder
proposed in (https://arxiv.org/abs/1802.04537).

Available samplers
-------------------

.. autosummary::
    ~XGen.samplers.NormalSampler
    ~XGen.samplers.GaussianMixtureSampler
    ~XGen.samplers.TwoStageVAESampler
    ~XGen.samplers.MAFSampler
    ~XGen.samplers.IAFSampler
    :nosignatures:

"""

from .piwae_config import PIWAEConfig
from .piwae_model import PIWAE

__all__ = ["PIWAE", "PIWAEConfig"]
