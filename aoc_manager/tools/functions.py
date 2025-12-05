from functools import cache


class String:
  @cache
  @staticmethod
  def chunk(string: str, chunk: int) -> list[str]:
    """Splits a string into chunks

    Source: https://stackoverflow.com/a/18854817
    
    Args:
      string (str): the string to chunk
      chunk (int): the size of each chunk
    
    Returns:
      chunks (list[str]): the string as a list of chunks
    """
    return [string[0+i:chunk+i] for i in range(0, len(string), chunk)]

class List:
  @staticmethod
  def are_items_equal(values: list[str]) -> bool:
    """Indicates whether all list values are equal
    
    Source: https://stackoverflow.com/a/3844948
    
    Args:
      values (list[str]): the input list
    
    Returns:
      list_items_equal (bool): indicates whether all list values are equal
    """
    return values.count(values[0]) == len(values)

class Number:
  @cache
  @staticmethod
  def does_it_repeat(num: int, chunk: int) -> bool:
    """Indicates whether a number repeats at all
    
    Args:
      num (int): the number to check
      chunk (int): size of substring to check
    
    Returns:
      repeats (bool): indicates whether it repeats
    """
    if chunk == 0:
      return False
    num_str: str = str(num)
    if len(num_str) % chunk != 0:
      return False
    if chunk == 1:
      return List.are_items_equal([c for c in num_str])
    return List.are_items_equal(String.chunk(num_str, chunk))
