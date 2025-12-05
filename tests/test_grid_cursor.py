from unittest import TestCase

from aoc_manager.tools.grid.cursor import GridCursor
from tests.testing_data.cursor import TestingData


class TestCursor(TestCase):
  """Contains unit tests for the Cursor dataclass"""
  td: TestingData = TestingData()

  def test_init(self) -> None:
    """
    GIVEN I have a Cursor class
    WHEN I instantiate it
    THEN it should instantiate as expected
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    assert isinstance(cursor, GridCursor)
    assert cursor.outside_bound_x == self.td.init_outside_bound_x
    assert cursor.outside_bound_y == self.td.init_outside_bound_y
    assert str(cursor) == self.td.class_str

  def test_as_tuple(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I get its coordinates as a tuple
    THEN it should be given as expected
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    assert cursor.as_tuple() == self.td.as_tuple
  
  def test_is_in_map(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I check if it is in the map
    THEN it should tell me correctly
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    assert cursor.is_in_map() == self.td.is_in_map

  def test_is_outside_bound_x(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I check if it is outside the x boundary
    THEN it should tell me correctly
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    assert cursor.is_outside_bound_x() == self.td.init_outside_bound_x
  
  def test_is_outside_bound_y(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I check if it is outside the y boundary
    THEN it should tell me correctly
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    assert cursor.is_outside_bound_y() == self.td.init_outside_bound_y
  
  def test_move_left(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I move it left
    THEN it should move left as expected
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    cursor.move_left()
    assert cursor.as_tuple() == self.td.left_result

  def test_move_up(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I move it up
    THEN it should move up as expected
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    cursor.move_up()
    assert cursor.as_tuple() == self.td.up_result

  def test_move_right(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I move it right
    THEN it should move right as expected
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    cursor.move_right()
    assert cursor.as_tuple() == self.td.right_result

  def test_move_down(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I move it down
    THEN it should move down as expected
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    cursor.move_down()
    assert cursor.as_tuple() == self.td.down_result

  def test_jump_to(self) -> None:
    """
    GIVEN I have a Cursor instance
    WHEN I jump the cursor to a new coordinate
    THEN it should move to that coordinate correctly
    """
    cursor: GridCursor = GridCursor(
      x=self.td.init_x,
      y=self.td.init_y,
      max_x=self.td.init_max_x,
      max_y=self.td.init_max_y
    )
    x, y = self.td.jump_to
    cursor.jump_to(x, y)
    assert cursor.as_tuple() == self.td.jump_to
  