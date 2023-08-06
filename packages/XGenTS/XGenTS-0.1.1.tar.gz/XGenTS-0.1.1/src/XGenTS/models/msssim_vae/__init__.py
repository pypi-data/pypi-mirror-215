"""This module is the implementation of the MSSSIM_VAE proposed in
(https://arxiv.org/abs/1511.06409).
This models uses a perceptual similarity metric for reconstruction.


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

from .msssim_vae_config import MSSSIM_VAEConfig
from .msssim_vae_model import MSSSIM_VAE

__all__ = ["MSSSIM_VAE", "MSSSIM_VAEConfig"]
