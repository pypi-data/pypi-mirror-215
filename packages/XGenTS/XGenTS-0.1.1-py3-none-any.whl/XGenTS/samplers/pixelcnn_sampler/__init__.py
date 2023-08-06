"""Sampler fitting a :class:`~XGen.models.normalizing_flows.PixelCNN` 
in the VQVAE's latent space.

Available models:
------------------

.. autosummary::
    ~XGen.models.VQVAE
    :nosignatures:
"""

from .pixelcnn_sampler import PixelCNNSampler
from .pixelcnn_sampler_config import PixelCNNSamplerConfig

__all__ = ["PixelCNNSampler", "PixelCNNSamplerConfig"]
