from unittest import TestCase

from aoc_manager.tools.grid.cursor import GridCursor
from aoc_manager.tools.grid.map import GridMap
from tests.testing_data.map import TestingData


class TestGridMap(TestCase):
  """Contains unit tests for the GridMap dataclass"""
  td: TestingData = TestingData()

  def test_init(self) -> None:
    """
    GIVEN I have a GridMap class
    WHEN I instantiate it
    THEN it should instantiate as expected
    """
    grid_map: GridMap = GridMap(
      input=self.td.init_input,
      start_at_y=self.td.init_start_at_y
    )
    assert isinstance(grid_map, GridMap)
    assert grid_map.input == self.td.init_input
    assert grid_map.start_at_x == 0
    assert grid_map.start_at_y == self.td.init_start_at_y
    assert grid_map.grid == self.td.init_grid_output
    assert grid_map.max_x == self.td.init_max_x
    assert grid_map.max_y == self.td.init_max_y
    assert isinstance(grid_map.cursor, GridCursor)

  def test_get(self) -> None:
    """
    GIVEN I have a GridMap
    WHEN I attempt to get it as a string
    THEN it should be retrieved as expected
    """
    grid_map: GridMap = GridMap(self.td.init_input)
    assert grid_map.get() == self.td.get_output
  
  def test_get_at_cursor(self) -> None:
    """
    GIVEN I have a GridMap
    WHEN I attempt to get the cursor value
    THEN it should be retrieved as expected
    """
    grid_map: GridMap = GridMap(self.td.init_input)
    assert grid_map.get_at_cursor() \
      == self.td.get_at_cursor
    grid_map.cursor.move_down()
    assert grid_map.get_at_cursor() \
      == self.td.get_at_cursor_down
    grid_map.cursor.move_left()
    assert grid_map.get_at_cursor() \
      == self.td.get_at_cursor_down_and_left

  def test_cursor_equals(self) -> None:
    """
    GIVEN I have a GridMap
    WHEN I attempt to validate its cursor value
    THEN it should validate as expected
    """
    grid_map: GridMap = GridMap(self.td.init_input)
    assert grid_map.cursor_equals(self.td.cursor_equals)
    grid_map.cursor.move_down()
    assert grid_map.cursor_equals(self.td.cursor_down_equals)

