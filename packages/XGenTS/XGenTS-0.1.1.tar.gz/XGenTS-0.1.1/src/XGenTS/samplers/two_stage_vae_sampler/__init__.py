"""Implementation of a Two Stage VAE sampler as proposed in 
(https://openreview.net/pdf?id=B1e0X3C9tQ).

Available models:
------------------

.. autosummary::
    ~XGen.models.VAE
    ~XGen.models.BetaVAE
    ~XGen.models.VAE_IAF
    ~XGen.models.DisentangledBetaVAE
    ~XGen.models.FactorVAE
    ~XGen.models.BetaTCVAE
    ~XGen.models.IWAE
    ~XGen.models.MSSSIM_VAE
    ~XGen.models.WAE_MMD
    ~XGen.models.INFOVAE_MMD
    ~XGen.models.VAMP
    ~XGen.models.VAEGAN
    ~XGen.models.HVAE
    ~XGen.models.RHVAE
    :nosignatures:

"""

from .two_stage_sampler import TwoStageVAESampler
from .two_stage_sampler_config import TwoStageVAESamplerConfig

__all__ = ["TwoStageVAESampler", "TwoStageVAESamplerConfig"]
