from dataclasses import dataclass, field


@dataclass
class GridCursor:
  x: int
  y: int
  max_x: int
  max_y: int
  outside_bound_x: bool = field(init=False)
  outside_bound_y: bool = field(init=False)

  def __post_init__(self) -> None:
    self.outside_bound_x: bool = self.is_outside_bound_x()
    self.outside_bound_y: bool = self.is_outside_bound_y()
  
  def as_tuple(self) -> tuple[int, int]:
    return (self.x, self.y)

  def is_in_map(self) -> bool:
    return not self.is_outside_bound_x() and not self.is_outside_bound_y()
  
  def is_outside_bound_x(self) -> bool:
    return self.x < 0 or self.x >= self.max_x

  def is_outside_bound_y(self) -> bool:
    return self.y < 0 or self.y >= self.max_y

  def move_left(self) -> None:
    self.x -= 1
    self.outside_bound_x = self.is_outside_bound_x()
  
  def move_up(self) -> None:
    self.y -= 1
    self.outside_bound_y = self.is_outside_bound_y()
  
  def move_right(self) -> None:
    self.x += 1
    self.outside_bound_x = self.is_outside_bound_x()
  
  def move_down(self) -> None:
    self.y += 1
    self.outside_bound_y = self.is_outside_bound_y()
  
  def jump_to(self, x: int, y: int) -> None:
    self.x = x
    self.y = y
    self.outside_bound_x = self.is_outside_bound_x()
    self.outside_bound_y = self.is_outside_bound_y()
  
  def __str__(self) -> str:
    return f'({self.x}, {self.y}) within ({self.max_x}, {self.max_y})'
