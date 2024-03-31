# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Configuration(Entity):
    """Configuration information """
    id: int = None
    directory: int = None
    env_map: str = None