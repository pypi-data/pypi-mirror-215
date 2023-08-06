"""This module is the implementation of a Info Variational Auto Encoder as proposed in 
(https://arxiv.org/abs/1706.02262)

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

from .info_vae_config import INFOVAE_MMD_Config
from .info_vae_model import INFOVAE_MMD

__all__ = ["INFOVAE_MMD", "INFOVAE_MMD_Config"]
