from importlib import import_module
from typing import Optional

from aoc_manager.tools.problem_solver import ProblemSolver


def import_solver(year: int, day: int) -> Optional[ProblemSolver]:
  """Retrieves a ProblemSolver based on a year and day, if it exists

  Args:
    year (int): the year of the solver
    day (int): the day of the solver

  Returns:
    solver (Optional[ProblemSolver]): if applicable, the applicable ProblemSolver
  """
  try:
    return getattr(
      import_module(f'solutions.Y{year}.solutions.d{day}'),
      f'D{day}Solver'
    )
  except ModuleNotFoundError:
    return None
