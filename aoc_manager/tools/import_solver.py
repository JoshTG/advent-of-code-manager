from importlib import import_module

from aoc_manager.tools.problem_solver import ProblemSolver


def import_solver(year: int, day: int) -> ProblemSolver | None:
  """Retrieves a ProblemSolver based on a year and day, if it exists

  Args:
    year (int): the year of the solver
    day (int): the day of the solver

  Returns:
    solver (ProblemSolver | None): if it exists, the applicable ProblemSolver
  """
  try:
    return getattr(
      import_module(f'solutions.Y{year}.solutions.d{day}'),
      f'D{day}Solver'
    )
  except ModuleNotFoundError:
    return None
