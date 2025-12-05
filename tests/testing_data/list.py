class ListTestingData:
  items_equal: list[tuple[list, bool]] = [
    (['a', 'a', 'a', 'a'], True),
    (['a', 'b'], False),
    (['1', 1], False),
    ([1, 1], True)
  ]
