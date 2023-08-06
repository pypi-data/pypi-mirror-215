"""This module is the implementation of a Poincaré Disk Variational Autoencoder
(https://arxiv.org/abs/1901.06033).

Available samplers
-------------------

.. autosummary::
    ~XGen.samplers.PoincareDiskSampler
    ~XGen.samplers.NormalSampler
    ~XGen.samplers.GaussianMixtureSampler
    ~XGen.samplers.TwoStageVAESampler
    ~XGen.samplers.MAFSampler
    ~XGen.samplers.IAFSampler
    :nosignatures:
"""

from .pvae_config import PoincareVAEConfig
from .pvae_model import PoincareVAE

__all__ = ["PoincareVAE", "PoincareVAEConfig"]
