from unittest import TestCase

from aoc_manager.tools.functions import List, Number, String
from tests.testing_data.list import ListTestingData
from tests.testing_data.number import NumberTestingData
from tests.testing_data.string import StringTestingData




class TestList(TestCase):
  """Contains unit tests for the List functions"""
  td: ListTestingData = ListTestingData()

  def test_are_items_equal(self) -> None:
    """
    GIVEN I have the are_items_equal method
    WHEN I attempt to check the equality of list items
    THEN it should check equality as expected
    """
    for values, output in self.td.items_equal:
      assert List.are_items_equal(values) == output

class TestNumber(TestCase):
  """Contains unit tests for the Number functions"""
  td: NumberTestingData = NumberTestingData()

  def test_does_it_repeat(self) -> None:
    """
    GIVEN I have the does_it_repeat method
    WHEN I attempt to see if a number repeats
    THEN it should tell me correctly
    """
    for num, chunk, output in self.td.does_it_repeat:
      assert Number.does_it_repeat(num, chunk) == output

class TestString(TestCase):
  """Contains unit tests for the String functions"""
  td: StringTestingData = StringTestingData()

  def test_chunk(self) -> None:
    """
    GIVEN I have the chunk() method
    WHEN I attempt to chunk a string
    THEN it should chunk as expected
    """
    for string, chunk, output in self.td.chunk:
      assert String.chunk(string, chunk) == output
