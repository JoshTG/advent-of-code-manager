class TestingData:
  init_input: list[list[str]] = [
    ['.', '.', '@', '@', '.'],
    ['@', '@', '@', '.', '@'],
    ['@', '@', '@', '@', '@'],
    ['@', '.', '@', '@', '@'],
    ['@', '@', '.', '@', '@']
  ]
  init_start_at_y: int = 2
  init_grid_output: dict[tuple[int, int], str] = {
    (0, 0): '.',
    (1, 0): '.',
    (2, 0): '@',
    (3, 0): '@',
    (4, 0): '.',
    (0, 1): '@',
    (1, 1): '@',
    (2, 1): '@',
    (3, 1): '.',
    (4, 1): '@',
    (0, 2): '@',
    (1, 2): '@',
    (2, 2): '@',
    (3, 2): '@',
    (4, 2): '@',
    (0, 3): '@',
    (1, 3): '.',
    (2, 3): '@',
    (3, 3): '@',
    (4, 3): '@',
    (0, 4): '@',
    (1, 4): '@',
    (2, 4): '.',
    (3, 4): '@',
    (4, 4): '@'
  }
  init_max_x: int = 5
  init_max_y: int = 5

  get_output: str = '..@@.\n@@@.@\n@@@@@\n@.@@@\n@@.@@\n'
  get_at_cursor: str = '.'
  get_at_cursor_down: str = '@'
  get_at_cursor_down_and_left: None = None

  cursor_equals: str = '.'
  cursor_down_equals: str= '@'