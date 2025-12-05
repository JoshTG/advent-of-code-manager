from dataclasses import dataclass, field

from aoc_manager.tools.grid.cursor import GridCursor


@dataclass
class GridMap:
  input: list[list[str]]
  start_at_x: int = field(default_factory=lambda: 0)
  start_at_y: int = field(default_factory=lambda: 0)
  grid: dict[tuple[int, int], str] = field(default_factory=lambda: {})

  max_x: int = field(init=False)
  max_y: int = field(init=False)
  cursor: GridCursor = field(init=False)

  def __post_init__(self) -> None:
    self.max_x: int = len(self.input[0])
    self.max_y: int = len(self.input)

    if not self.grid:
      for y in range(self.max_y):
        for x in range(self.max_x):
          self.grid[(x, y)] = self.input[y][x]
    
    self.cursor: GridCursor = GridCursor(
      x=self.start_at_x,
      y=self.start_at_y,
      max_x=self.max_x,
      max_y=self.max_y
    )

  def get(self) -> str:
    full_map: str = ''
    for coordinate, sign in self.grid.items():
      full_map += sign
      if coordinate[0] == self.max_x - 1:
        full_map += '\n'
    return full_map
  
  def get_at_cursor(self) -> str | None:
    if self.cursor.is_outside_bound_x():
      return None
    if self.cursor.is_outside_bound_y():
      return None
    return self.grid[self.cursor.as_tuple()]

  def cursor_equals(self, value: str) -> bool:
    return self.cursor.is_in_map() and self.get_at_cursor() == value
