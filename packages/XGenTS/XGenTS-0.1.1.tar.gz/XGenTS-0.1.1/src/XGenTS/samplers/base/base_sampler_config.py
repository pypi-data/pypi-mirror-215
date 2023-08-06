from pydantic.dataclasses import dataclass

from XGen.config import BaseConfig


@dataclass
class BaseSamplerConfig(BaseConfig):
    """
    BaseSampler config class.
    """

    pass
