import polars as pl

from dataclasses import field, dataclass
from time import time
from typing import Any
from uuid import uuid4

from aoc_manager.tables.input import \
  table as tab_aoc_input
from aoc_manager.tables.log import \
  table as tab_aoc_log


@dataclass
class ProblemSolver:
  """Class that contains the code and metadata around an AoC solution for a day"""
  year: str
  day: str
  test: bool
  debug: bool
  input_format: type
  mask_answers: bool = field(default_factory=lambda: False)
  processing_rounding_digits: int = field(default_factory=lambda: 8)

  log_level_map: dict[str, str] = field(init=False)
  
  input_a_text: str = field(init=False)
  input_b_text: str = field(init=False)
  
  answer_a: Any = field(init=False)
  answer_b: Any = field(init=False)

  expected_a: str = field(init=False)
  expected_b: str = field(init=False)
  
  preprocessing_time: float = field(init=False)
  a_processing_time: float = field(init=False)
  b_processing_time: float = field(init=False)
  total_processing_time: float = field(init=False)
  
  run_id_a: str = field(init=False)
  run_id_b: str = field(init=False)
  
  context: str = field(init=False)

  def __post_init__(self) -> None:
    self.log_level_map: dict[str, str] = {
      'p': 'Pre-Processor',
      'a': 'Part A',
      'b': 'Part B'
    }
    self.input_a_text, self.input_b_text, \
      self.expected_a, self.expected_b = self._retrieve_inputs()

    self.answer_a: Any = None
    self.answer_b: Any = None

    self.preprocessing_time: float = 0.00
    self.a_processing_time: float = 0.00
    self.b_processing_time: float = 0.00
    self.total_processing_time: float = 0.00

    self.run_id_a: str = ''
    self.run_id_b: str = ''

    self.context: str = ''
    self.logs: list[dict] = []

  def preprocess_inputs(self) -> None:
    """Log and execute the _preprocess() method"""
    if len(self.input_a_text) == 0 and len(self.input_b_text) == 0:
      raise RuntimeError('Error: no input text has been provided.')

    preprocessing_start_time: float = time()
    self.context: str = 'p'
    self._preprocess()
    self.preprocessing_time: float = max(time() - preprocessing_start_time, 0.00)
    self.save_logs()
    
  def run_a(self) -> None:
    """Log and execute the _solve_a() method"""
    a_start_time: float = time()
    self.context: str = 'a'
    self.run_id_a: str = str(uuid4())
    self._solve_a()
    self.a_processing_time: float = max(time() - a_start_time, 0.00)
    self.total_processing_time: float = self.get_total_processing_time()
    self.save_logs()

  def run_b(self) -> None:
    """Log and execute the _solve_b() method"""
    b_start_time: float = time()
    self.context: str = 'b'
    self.run_id_b: str = str(uuid4())
    self._solve_b()
    self.b_processing_time: float = max(time() - b_start_time, 0.00)
    self.total_processing_time: float = self.get_total_processing_time()
    self.save_logs()

  def log(self, line: Any, label: str = '') -> None:
    """Store a log with context
    
    Args:
      line (Any): the line to log
      label (str): Any helpful context with which to tag the line
    """
    if not self.debug:
      return
    self.logs.append({
      'year': int(self.year),
      'day': int(self.day),
      'context': self.log_level_map.get(self.context, ''),
      'data': str(line),
      'label': label
    })
  
  def save_logs(self) -> None:
    """Saves logs to Polta Table"""
    tab_aoc_log.append(self.logs)
    self.logs.clear()

  def get_total_processing_time(self) -> float:
    """Retrieves the total processing time of the execution steps
    
    Tracked methods:
      1. Pre-Processor
      2. Part A
      3. Part B

    Returns:
      total_processing_time (float): the total processing time of the three main methods
    """
    return max(
      self.preprocessing_time + self.a_processing_time + self.b_processing_time,
      0.00
    )

  def _preprocess(self) -> None:
    """This should get overriden by a child class"""  
    pass
      
  def _solve_a(self) -> None:
    """This should get overriden by a child class"""
    pass

  def _solve_b(self) -> None:
    """This should get overriden by a child class"""
    pass

  def _retrieve_inputs(self) -> tuple[str, str, str, str]:
    """Retrieves the proper inputs for the day and Any test data
    
    Returns:
      inputs (tuple[str, str, str, str]): input A, expected A, input B, expected B
    """
    row: dict[str, Any] = (tab_aoc_input
      .get(
        filter_conditions={'year': int(self.year), 'day': int(self.day)}
      ).with_columns(pl
        .when(pl.col('input_test_b') != '')
        .then(pl.col('input_test_b'))
        .otherwise(pl.col('input_test_a'))
        .alias('input_test_b')
      ).to_dicts()
      [0]
    )

    cols: list[str] = ['input_test_a', 'input_test_b'] if self.test else \
      ['full_input', 'full_input']

    inputs: list[str] = []

    for col in cols:
      if self.input_format is str:
        inputs.append(row[col])
        continue

      items: list[str] = list(map(lambda l: l.replace('\n', ''), row[col].splitlines()))

      if self.input_format == list[str]:
        inputs.append(items)
      elif self.input_format == list[list[int]]:
        inputs.append(list(map(lambda l: [int(i) for i in l], items)))
      elif self.input_format == list[list[str]]:
        inputs.append(list(map(lambda l: [i for i in l], items)))
      elif self.input_format is not None:
        inputs.append(list(map(lambda i: self.input_format(i) if i != '' else -1, items)))
      else:
        raise NotImplementedError
    
    return inputs[0], inputs[1], row['expected_a'], row['expected_b']
