class NumberTestingData:
  does_it_repeat: list[tuple[int, int, bool]] = [
    (1, 1, True),
    (12, 1, False),
    (11, 1, True),
    (112, 1, False),
    (333, 1, True),
    (1010, 1, False),
    (1010, 2, True),
    (10000, 1, False),
    (11111, 1, True),
    (123123, 3, True),
    (123123, 2, False),
    (123123, 5, False),
    (1188511885, 5, True),
    (1188511885, 2, False),
    (1188511885, 3, False),
    (1188511885, 4, False)
  ]
