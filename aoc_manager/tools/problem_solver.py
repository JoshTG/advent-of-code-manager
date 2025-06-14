from os import getcwd, path
from time import time
from uuid import uuid4

from aoc_manager.tools.log import Log


class ProblemSolver:
  """Class that contains the code and metadata around an AoC solution for a day"""

  # Constant variables related to directory paths for inputs and outputs
  INPUT_PATH_PREFIX: str = path.join(getcwd(), 'assets', 'inputs')
  OUTPUT_PATH_PREFIX: str = path.join(getcwd(), 'assets', 'outputs')

  # Constant variables related to processing context and output
  PROCESSING_ROUNDING_DIGITS: int = 8
  LOG_LEVEL_MAP: dict[str, str] = {
      'p': 'Pre-Processor',
      'a': 'Part A',
      'b': 'Part B'
  }

  def __init__(self, year: str, day: str, test: bool, debug: bool, input_format: type = str,
                mask_answers: bool = False) -> None:
    if not isinstance(year, str):
        raise TypeError('Error: year must be of type <str>')
    if not isinstance(day, str):
        raise TypeError('Error: day must be of type <str>')
    if not isinstance(test, bool):
        raise TypeError('Error: test must be of type <bool>')
    if not isinstance(debug, bool):
        raise TypeError('Error: debug must be of type <bool>')
    
    # Store the input arguments
    self.year: str = year
    self.day: str = day
    self.test: bool = test
    self.debug: bool = debug
    self.mask_answers: bool = mask_answers

    # Build the path prefixes and file names for inputs and outputs
    self.input_path_prefix: str = self._build_input_path_prefix()
    self.output_path_prefix: str = self._build_output_path_prefix()
    self.input_format: type = input_format
    self.filename: str = path.join(self.input_path_prefix, f'{self.day}.txt')
    self.filename_a_test: str = path.join(self.input_path_prefix, f'{self.day}-a-test.txt')
    self.filename_b_test: str = path.join(self.input_path_prefix, f'{self.day}-b-test.txt')
    self.input_a_text, self.input_b_text = self._retrieve_inputs()

    # Variables that contain the results
    self.answer_a: any = None
    self.answer_b: any = None

    # Variables containing processing time for tracking performance
    self.preprocessing_time: float = 0.00
    self.a_processing_time: float = 0.00
    self.b_processing_time: float = 0.00
    self.total_processing_time: float = 0.00

    # Variables for unique Run IDs for tracking solutions and verified answers
    self.run_id_a: str = ''
    self.run_id_b: str = ''

    # Variables for logging and context tracking 
    self.logs: list[Log] = []
    self.context: str = ''

  def preprocess_inputs(self) -> None:
    """Log and execute the _preprocess() method"""
    preprocessing_start_time: float = time()
    self.context: str = 'p'
    self._preprocess()
    self.preprocessing_time: float = time() - preprocessing_start_time
    
  def run_a(self) -> None:
    """Log and execute the _solve_a() method"""
    a_start_time: float = time()
    self.context: str = 'a'
    self.run_id_a: str = str(uuid4())
    self._solve_a()
    self.a_processing_time: float = time() - a_start_time
    self.total_processing_time: float = self.get_total_processing_time()

  def run_b(self) -> None:
    """Log and execute the _solve_b() method"""
    b_start_time: float = time()
    self.context: str = 'b'
    self.run_id_b: str = str(uuid4())
    self._solve_b()
    self.b_processing_time: float = time() - b_start_time
    self.total_processing_time: float = self.get_total_processing_time()

  def log(self, line: any, label: str = '', also_print: bool = False) -> None:
    """Store a log with context and optionally print it
    
    Args:
      line (any): the line to log
      label (str): any helpful context with which to tag the line
      also_print (optional) (bool): indicates whether to print in addition to logging
    """
    log: Log = Log(
      data=str(line),
      label=label,
      level=self.LOG_LEVEL_MAP.get(self.context, '')
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
    return self.preprocessing_time + self.a_processing_time + self.b_processing_time

  def _preprocess(self) -> None:
    """This should get overriden by a child class"""  
    pass
      
  def _solve_a(self) -> None:
    """This should get overriden by a child class"""
    pass

  def _solve_b(self) -> None:
    """This should get overriden by a child class"""
    pass

  def _retrieve_inputs(self) -> None:
    """Retrieves the proper inputs for the day and any test data"""
    input_a_path: str = path.join(self.input_path_prefix, self.filename_a_test if self.test else self.filename)
    input_b_path: str = path.join(self.input_path_prefix, self.filename_b_test if self.test else self.filename)

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

  def _build_input_path_prefix(self) -> str:
    """Builds the full path for the inputs directory
    
    Returns:
      input_path_prefix (str): the full path of the inputs directory
    """
    return path.join(getcwd(), 'solutions', f'Y{self.year}', 'inputs')

  def _build_output_path_prefix(self) -> str:
    """Builds the full path for the outputs directory
    
    Returns:
      output_path_prefix (str): the full path of the outputs directory
    """
    return path.join(getcwd(), 'solutions', f'Y{self.year}', 'outputs')
