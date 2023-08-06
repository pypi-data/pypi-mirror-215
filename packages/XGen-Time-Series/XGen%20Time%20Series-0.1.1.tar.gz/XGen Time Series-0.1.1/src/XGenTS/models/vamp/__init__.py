"""This module is the implementation of a Variational Mixture of Posterior prior 
Variational Auto Encoder proposed in (https://arxiv.org/abs/1705.07120).

Available samplers
-------------------

.. autosummary::
    ~XGen.samplers.NormalSampler
    ~XGen.samplers.GaussianMixtureSampler
    ~XGen.samplers.TwoStageVAESampler
    ~XGen.samplers.VAMPSampler
    ~XGen.samplers.MAFSampler
    ~XGen.samplers.IAFSampler
    :nosignatures:
"""

from .vamp_config import VAMPConfig
from .vamp_model import VAMP

__all__ = ["VAMP", "VAMPConfig"]
