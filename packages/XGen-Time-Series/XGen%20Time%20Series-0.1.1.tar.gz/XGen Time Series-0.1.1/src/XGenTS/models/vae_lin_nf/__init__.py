"""This module is the implementation of a Variational Auto Encoder with Normalizing Flow
(https://arxiv.org/pdf/1505.05770.pdf).

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

from .vae_lin_nf_config import VAE_LinNF_Config
from .vae_lin_nf_model import VAE_LinNF

__all__ = ["VAE_LinNF", "VAE_LinNF_Config"]
