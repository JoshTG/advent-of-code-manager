class StringTestingData:
  chunk: list[tuple[str, int, list]] = [
    ('ababab', 2, ['ab', 'ab', 'ab']),
    ('abcdef', 3, ['abc', 'def']),
    ('abcdefghijk', 2, ['ab', 'cd', 'ef', 'gh', 'ij', 'k'])
  ]
