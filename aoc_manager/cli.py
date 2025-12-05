import polars as pl

from enum import Enum
from typer import Argument, Typer

from aoc_manager.tools.import_solver import import_solver
from aoc_manager.tools.problem_solver import ProblemSolver


class Parts(Enum):
  A: str = 'a'
  B: str = 'b'
  BOTH: str = 'both'


app: Typer = Typer()

run_app: Typer = Typer()
app.add_typer(run_app, name='run')

@run_app.command('solution')
def run_solution(year: int, day: int,
                 parts: Parts = Argument(default=Parts.BOTH),
                 test: bool = Argument(default=False)) -> None:
  solver: ProblemSolver = import_solver(year, day)
  if not solver:
    raise RuntimeError('Error: solver not found')
  solver: ProblemSolver = solver(
    year=str(year),
    debug=False,
    mask_answers=False,
    test=test
  )

  rows: list[dict] = []
  solver.preprocess_inputs()
  if parts.value in [Parts.A.value, Parts.BOTH.value]:
    solver.run_a()
    rows.append({'Part': 'A', 'Solution': solver.answer_a, 'Processing Time': solver.a_processing_time})
  if parts.value in [Parts.B.value, Parts.BOTH.value]:
    solver.run_b()
    rows.append({'Part': 'B', 'Solution': solver.answer_b, 'Processing Time': solver.b_processing_time})
  print(f'Pre-processing time: {round(solver.preprocessing_time, 5)}s')
  print(f'Total processing time: {round(solver.total_processing_time, 5)}s')
  print(pl.DataFrame(rows))


if __name__ == '__main__':
  app()
