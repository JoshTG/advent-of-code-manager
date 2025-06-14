import polars as pl

from datetime import datetime
from pyperclip import copy as copy_to_clipboard
from shiny import (
  Inputs,
  module,
  Outputs,
  reactive,
  render,
  Session,
  ui
)
from shiny.reactive import Value
from shiny.ui import Tag

from aoc_manager.tables.answer import table as pt_can_answer
from aoc_manager.tables.solution import table as pt_can_solution
from aoc_manager.tools.import_solver import import_solver
from aoc_manager.tools.problem_solver import ProblemSolver


# Define reactive values for the solver page
solution_data: Value = Value({})
a_debug: Value = Value('')
b_debug: Value = Value('')
a_output: Value = Value('')
b_output: Value = Value('')


@module.server
def solver_server(input: Inputs, output: Outputs, session: Session) -> None:
  @reactive.effect
  def _() -> None:
    """Generic reactive effects for site use"""
    year: int = input.num_year()
    day: int = input.num_day()
    solver: ProblemSolver | None = import_solver(year, day)
    ui.update_action_button('btn_run', disabled=solver is None)
    
  @render.text
  def txt_day_information() -> str:
    """Renders the header for the solution card
    
    Returns:
      header (str): the header indicating the year and day of the solution
    """
    return f'Advent of Code {input.num_year()}: Day {input.num_day()}'

  @reactive.effect
  @reactive.event(input.btn_run)
  def btn_run() -> None:
    year: int = input.num_year()
    day: int = input.num_day()
    debug: bool = input.chk_debug()
    mask_answers: bool = input.chk_mask_answers()
    test: bool = input.chk_test()
    selection: str = input.sel_day_part()

    solver: ProblemSolver = import_solver(year, day)(
      year=str(year),
      debug=debug,
      mask_answers=mask_answers,
      test=test
    )

    solver.preprocess_inputs()

    if selection in ['a', 'both']:
      solver.run_a()
      a_output.set('X'*len(str(solver.answer_a)) if solver.mask_answers else solver.answer_a)
      pt_can_solution.append({
        '_execution_ts': datetime.now(),
        'id': solver.run_id_a,
        'year': year,
        'day': day,
        'part': 'a',
        'test_ind': test,
        'answer': str(solver.answer_a),
        'processing_time': solver.a_processing_time
      })
    if selection in ['b', 'both']:
      solver.run_b()
      b_output.set('X'*len(str(solver.answer_b)) if solver.mask_answers else solver.answer_b)
      pt_can_solution.append({
        '_execution_ts': datetime.now(),
        'id': solver.run_id_b,
        'year': year,
        'day': day,
        'part': 'b',
        'test_ind': test,
        'answer': str(solver.answer_b),
        'processing_time': solver.b_processing_time
      })
    solution_data.set(solver.__dict__)

  @reactive.effect
  @reactive.event(input.btn_copy_a)
  def btn_copy_a() -> None:
    data: dict = solution_data.get()

    if not data.get('answer_a'):
      ui.notification_show(
        'Error: No answer generated.',
        type='error',
        duration=3
      )
      return

    copy_to_clipboard(data.get('answer_a'))
    ui.notification_show(
      f'Part A answer was copied to clipboard!',
      type='message',
      duration=2
    )
  
  @reactive.effect
  @reactive.event(input.btn_save_a)
  def btn_save_a() -> None:
    data: dict = solution_data.get()

    if not data.get('year'):
      ui.notification_show(
        f'Error: No answer found. Please click \'Run\' to generate an answer.',
        type='error',
        duration=3
      )
      return

    df: pl.DataFrame = pl.DataFrame(
      data=[{
        'year': int(data['year']),
        'day': int(data['day']),
        'part': 'a',
        'test_ind': input.chk_test(),
        'solution_id': data['run_id_a'],
        'answer': str(data['answer_a'])
      }],
      schema=pt_can_answer.schema_polars
    )
    pt_can_answer.save_to_delta(df)
    ui.notification_show(
      f'Answer A saved!',
      type='message',
      duration=2
    )

  @reactive.effect
  @reactive.event(input.btn_copy_b)
  def btn_copy_b() -> None:
    data: dict = solution_data.get()

    if not data.get('answer_b'):
      ui.notification_show(
        'Error: No answer generated.',
        type='error',
        duration=3
      )
      return

    copy_to_clipboard(data.get('answer_b'))
    ui.notification_show(
      f'Part B answer was copied to clipboard!',
      type='message',
      duration=2
    )

  @reactive.effect
  @reactive.event(input.btn_save_b)
  def btn_save_b() -> None:
    data: dict = solution_data.get()

    if not data.get('year'):
      ui.notification_show(
        f'Error: No answer found. Please click \'Run\' to generate an answer.',
        type='error',
        duration=3
      )
      return

    df: pl.DataFrame = pl.DataFrame(
      data=[{
        'year': int(data['year']),
        'day': int(data['day']),
        'part': 'b',
        'test_ind': input.chk_test(),
        'solution_id': data['run_id_b'],
        'answer': str(data['answer_b'])
      }],
      schema=pt_can_answer.schema_polars
    )
    pt_can_answer.upsert(df)
    ui.notification_show(
      f'Answer B saved!',
      type='message',
      duration=2
    )


  @render.data_frame
  def tbl_debug() -> render.DataTable:
    data: dict[str, any] = solution_data.get()
    logs: list[dict[str, any]] = data['logs'] if data.get('debug', False) else []
    return render.DataTable(
      data=pl.DataFrame(logs),
      width='100%',
      height='300px',
      filters=True,
      summary=False
    )

  @render.ui
  def txt_a_output() -> Tag:
    data: dict = solution_data.get()
    a_output: str = data.get('answer_a', '')
    mask_answer: bool = data.get('mask_answers', False)
    if a_output:
      return ui.h2(f'Answer: {"X"*len(str(a_output)) if mask_answer else a_output}')
    return ui.h2('')

  @render.ui
  def txt_preprocessing_time() -> Tag:
    data: dict = solution_data.get()
    preprocessing_time: float = data.get('preprocessing_time')
    if preprocessing_time is not None:
      return ui.h5(f'Preprocessing time: {round(preprocessing_time, 5)}s')
    return ui.h5('')

  @render.ui
  def txt_total_processing_time() -> Tag:
    data: dict = solution_data.get()
    total_time: float = data.get('total_processing_time')
    if total_time is not None:
      return ui.h4(f'Total processing time: {round(total_time, 5)}s')
    return ui.h4('')
  
  @render.ui
  def txt_a_processing_time() -> Tag:
    data: dict = solution_data.get()
    a_time: float = data.get('a_processing_time')
    if a_time is not None:
      return ui.h4(f'Processing time: {round(a_time, 5)}s')
    return ui.h4('')

  @render.ui
  def txt_b_output() -> Tag:
    data: dict = solution_data.get()
    b_output: str = data.get('answer_b', '')
    mask_answer: bool = data.get('mask_answers', False)
    if b_output:
      return ui.h2(f'Answer: {"X"*len(str(b_output)) if mask_answer else b_output}')
    return ui.h2('')

  @render.ui
  def txt_b_processing_time() -> Tag:
    data: dict = solution_data.get()
    a_time: float = data.get('b_processing_time')
    if a_time is not None:
      return ui.h4(f'Processing time: {round(a_time, 5)}s')
    return ui.h4('')
