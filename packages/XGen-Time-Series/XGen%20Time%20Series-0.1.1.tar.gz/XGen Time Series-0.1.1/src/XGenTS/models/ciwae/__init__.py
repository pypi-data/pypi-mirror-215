"""This module is the implementation of the Combination Importance Weighted Autoencoder
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

from .ciwae_config import CIWAEConfig
from .ciwae_model import CIWAE

__all__ = ["CIWAE", "CIWAEConfig"]
