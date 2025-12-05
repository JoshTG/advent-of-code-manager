from dataclasses import dataclass, field
from yaml import safe_load


@dataclass
class Config:
  data_path: str = field(init=False)

  def __post_init__(self) -> None:
    config: dict = safe_load('config.yaml')
    
    self.data_path: str = config.get('data_path', 'AoC/')