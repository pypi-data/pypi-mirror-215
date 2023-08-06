"""This module is the implementation of the Multiply Importance Weighted Autoencoder
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

from .miwae_config import MIWAEConfig
from .miwae_model import MIWAE

__all__ = ["MIWAE", "MIWAEConfig"]
