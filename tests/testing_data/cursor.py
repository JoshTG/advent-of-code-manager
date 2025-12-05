class TestingData:
  init_x: int = 0
  init_y: int = 6
  init_max_x: int = 5
  init_max_y: int = 5
  init_outside_bound_x: bool = False
  init_outside_bound_y: bool = True
  class_str: str = '(0, 6) within (5, 5)'

  as_tuple: tuple[int, int] = (0, 6)
  is_in_map: bool = False

  left_result: tuple[int, int] = (-1, 6)
  up_result: tuple[int, int] = (0, 5)
  right_result: tuple[int, int] = (1, 6)
  down_result: tuple[int, int] = (0, 7)

  jump_to: tuple[int, int] = (4, 3)