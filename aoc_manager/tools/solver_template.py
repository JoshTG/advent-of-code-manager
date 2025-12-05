solver_template: str = '''from aoc_manager.tools.problem_solver import ProblemSolver


class D{day}Solver(ProblemSolver):
  def __init__(self, year: str, test: bool = False, debug: bool = False, input_format: type = str,
               mask_answers: bool = False) -> None:
    super().__init__(
      year=year,
      day='{day}',
      test=test,
      debug=debug,
      input_format=input_format,
      mask_answers=mask_answers
    )

    self.answer_a: int = 0
    self.answer_b: int = 0

  def _preprocess(self) -> None:
    pass

  def _solve_a(self) -> None:
    raise NotImplementedError('Solver A not implemented yet.')

  def _solve_b(self) -> None:
    raise NotImplementedError('Solver B not implemented yet.')
'''