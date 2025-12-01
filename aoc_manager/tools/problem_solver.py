from dataclasses import field, dataclass
from os import getcwd, path
from time import time
from typing import Any
from uuid import uuid4

from aoc_manager.tools.log import Log


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

  input_path_prefix: str = field(init=False)
  output_path_prefix: str = field(init=False)
  log_level_map: dict[str, str] = field(init=False)
  
  filename: str = field(init=False)
  filename_a_test: str = field(init=False)
  filename_b_test: str = field(init=False)
  
  input_a_text: str = field(init=False)
  input_b_text: str = field(init=False)
  
  answer_a: Any = field(init=False)
  answer_b: Any = field(init=False)
  
  preprocessing_time: float = field(init=False)
  a_processing_time: float = field(init=False)
  b_processing_time: float = field(init=False)
  total_processing_time: float = field(init=False)
  
  run_id_a: str = field(init=False)
  run_id_b: str = field(init=False)
  
  logs: list[Log] = field(init=False)
  context: str = field(init=False)

  def __post_init__(self) -> None:
    self.input_path_prefix: str = path.join(
      getcwd(),
      'solutions',
      f'Y{self.year}',
      'inputs'
    )
    self.output_path_prefix: str = path.join(
      getcwd(),
      'solutions',
      f'Y{self.year}',
      'outputs'
    )
    self.log_level_map: dict[str, str] = {
      'p': 'Pre-Processor',
      'a': 'Part A',
      'b': 'Part B'
    }

    self.filename: str = path.join(
      self.input_path_prefix,
      f'{self.day}.txt'
    )
    self.filename_a_test: str = path.join(
      self.input_path_prefix,
      f'{self.day}-a-test.txt'
    )
    self.filename_b_test: str = path.join(
      self.output_path_prefix,
      f'{self.day}-b-test.txt'
    )
    self.input_a_text, self.input_b_text = self._retrieve_inputs()

    self.answer_a: Any = None
    self.answer_b: Any = None

    self.preprocessing_time: float = 0.00
    self.a_processing_time: float = 0.00
    self.b_processing_time: float = 0.00
    self.total_processing_time: float = 0.00

    self.run_id_a: str = ''
    self.run_id_b: str = ''

    self.logs: list[Log] = []
    self.context: str = ''

  def preprocess_inputs(self) -> None:
    """Log and execute the _preprocess() method"""
    preprocessing_start_time: float = time()
    self.context: str = 'p'
    self._preprocess()
    self.preprocessing_time: float = max(time() - preprocessing_start_time, 0.00)
    
  def run_a(self) -> None:
    """Log and execute the _solve_a() method"""
    a_start_time: float = time()
    self.context: str = 'a'
    self.run_id_a: str = str(uuid4())
    self._solve_a()
    self.a_processing_time: float = max(time() - a_start_time, 0.00)
    self.total_processing_time: float = self.get_total_processing_time()

  def run_b(self) -> None:
    """Log and execute the _solve_b() method"""
    b_start_time: float = time()
    self.context: str = 'b'
    self.run_id_b: str = str(uuid4())
    self._solve_b()
    self.b_processing_time: float = max(time() - b_start_time, 0.00)
    self.total_processing_time: float = self.get_total_processing_time()

  def log(self, line: Any, label: str = '', also_print: bool = False) -> None:
    """Store a log with context and optionally print it
    
    Args:
      line (Any): the line to log
      label (str): Any helpful context with which to tag the line
      also_print (optional) (bool): indicates whether to print in addition to logging
    """
    log: Log = Log(
      data=str(line),
      label=label,
      level=self.log_level_map.get(self.context, '')
    )
    self.logs.append(log)

    if also_print:
      log.print()

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

  def _retrieve_inputs(self) -> tuple[str, str]:
    """Retrieves the proper inputs for the day and Any test data
    
    Returns:
      inputs (tuple[str, str]): the inputs of A and B
    """
    if self.test:
      input_a_path: str = path.join(self.input_path_prefix, self.filename_a_test)
      input_b_path: str = path.join(self.input_path_prefix, self.filename_b_test)
    else:
      input_a_path: str = path.join(self.input_path_prefix, self.filename)
      input_b_path: str = path.join(self.input_path_prefix, self.filename)

    if not path.exists(input_b_path):
      input_b_path: str = input_a_path

    inputs: list[str] = []

    for input_path in [input_a_path, input_b_path]:
      if self.input_format == str:
        inputs.append(open(input_path, 'r').read())
        continue

      items: list[str] = list(map(lambda l: l.replace('\n', ''), open(input_path, 'r').readlines()))

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
    
    return inputs
