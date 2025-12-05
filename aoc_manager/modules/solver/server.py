import polars as pl
import traceback

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
from typing import Optional

from aoc_manager.tables.guess import \
  table as tab_std_guess
from aoc_manager.tables.log import \
  table as tab_std_log
from aoc_manager.tables.solution import \
  table as tab_can_solution
from aoc_manager.tools.import_solver import import_solver
from aoc_manager.tools.problem_solver import ProblemSolver


# Define reactive values for the solver page
solution_data: Value = Value({})
debug_logs_pre: Value = Value([])
debug_logs_a: Value = Value([])
debug_logs_b: Value = Value([])
error_message_pre: Value = Value('')
error_message_a: Value = Value('')
error_message_b: Value = Value('')


@module.server
def solver_server(input: Inputs, output: Outputs, session: Session) -> None:
  @reactive.effect
  def _() -> None:
    """Generic reactive effects for site use"""
    year: int = input.num_year()
    day: int = input.num_day()
    data: dict = solution_data.get()
    solution_a_exists: bool = data.get('answer_a', None) is not None
    solution_b_exists: bool = data.get('answer_a', None) is not None
    is_test: bool = data.get('test', False)
    solver: Optional[ProblemSolver] = import_solver(year, day)
    ui.update_action_button('btn_run', disabled=solver is None)
    ui.update_action_button('btn_fetch_debug_logs_pre', disabled=data == {})
    ui.update_action_button('btn_fetch_debug_logs_a', disabled=not solution_a_exists)
    ui.update_action_button('btn_fetch_debug_logs_b', disabled=not solution_b_exists)
    ui.update_action_button('btn_a_too_low', disabled=not solution_a_exists or is_test)
    ui.update_action_button('btn_a_correct', disabled=not solution_a_exists or is_test)
    ui.update_action_button('btn_a_too_high', disabled=not solution_a_exists or is_test)
    ui.update_action_button('btn_b_too_low', disabled=not solution_b_exists or is_test)
    ui.update_action_button('btn_b_correct', disabled=not solution_b_exists or is_test)
    ui.update_action_button('btn_b_too_high', disabled=not solution_b_exists or is_test)

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
    solution_data.set({})
    error_message_pre.set('')
    error_message_a.set('')
    error_message_b.set('')
    tab_std_log.truncate()

    try:
      solver: ProblemSolver = import_solver(year, day)(
        year=str(year),
        debug=debug,
        mask_answers=mask_answers,
        test=test
      )
    except FileNotFoundError:
      error_message_pre.set(traceback.format_exc())
      ui.notification_show(
        'Error during solver import: Please read error message for traceback.',
        duration=3,
        type='error'
      )
      return

    try:
      solver.preprocess_inputs()
    except Exception:
      error_message_pre.set(traceback.format_exc())
      ui.notification_show(
        'Error during pre-processing: Please read error message for traceback.',
        duration=3,
        type='error'
      )
    else:
      if selection in ['a', 'both']:
        try:
          solver.run_a()
        except Exception:
          error_message_a.set(traceback.format_exc())
          ui.notification_show(
            'Error during A: Please read error message for traceback.',
            duration=3,
            type='error'
          )
        else:
          tab_can_solution.append({
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
        try:
          solver.run_b()
        except Exception:
          error_message_b.set(traceback.format_exc())
          ui.notification_show(
            'Error during B: Please read error message for traceback.',
            duration=3,
            type='error'
          )
        else:
          tab_can_solution.append({
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
  @reactive.event(input.btn_fetch_debug_logs_pre)
  def btn_fetch_debug_logs_pre() -> None:
    limit: int = input.num_max_logs_pre()
    df: pl.DataFrame = tab_std_log.get(
      filter_conditions={
        'year': input.num_year(),
        'day': input.num_day(),
        'context': 'Pre-Processor'
      },
      select=['data', 'label', 'context'],
      limit=limit
    )
    debug_logs_pre.set(df.to_dicts())

  @reactive.effect
  @reactive.event(input.btn_fetch_debug_logs_a)
  def btn_fetch_debug_logs_a() -> None:
    limit: int = input.num_max_logs_a()
    df: pl.DataFrame = tab_std_log.get(
      filter_conditions={
        'year': input.num_year(),
        'day': input.num_day(),
        'context': 'Part A'
      },
      select=['data', 'label', 'context'],
      limit=limit
    )
    debug_logs_a.set(df.to_dicts())

  @reactive.effect
  @reactive.event(input.btn_fetch_debug_logs_b)
  def btn_fetch_debug_logs_b() -> None:
    limit: int = input.num_max_logs_b()
    df: pl.DataFrame = tab_std_log.get(
      filter_conditions={
        'year': input.num_year(),
        'day': input.num_day(),
        'context': 'Part B'
      },
      select=['data', 'label', 'context'],
      limit=limit
    )
    debug_logs_b.set(df.to_dicts())

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
      'Part A answer was copied to clipboard!',
      type='message',
      duration=2
    )

  @reactive.effect
  @reactive.event(input.btn_a_too_low)
  def btn_a_too_low() -> None:
    data: dict = solution_data.get()
    tab_std_guess.upsert({
      'year': input.num_year(),
      'day': input.num_day(),
      'part': 'A',
      'solution_id': data['run_id_a'],
      'guess': str(data['answer_a']),
      'comparison': 'l'
    })
    ui.notification_show(
      'Guess saved!',
      duration=2,
      type='message'
    )

  @reactive.effect
  @reactive.event(input.btn_a_correct)
  def btn_a_correct() -> None:
    data: dict = solution_data.get()
    tab_std_guess.upsert({
      'year': input.num_year(),
      'day': input.num_day(),
      'part': 'A',
      'solution_id': data['run_id_a'],
      'guess': str(data['answer_a']),
      'comparison': 'c'
    })
    ui.notification_show(
      'Guess saved!',
      duration=2,
      type='message'
    )

  @reactive.effect
  @reactive.event(input.btn_a_too_high)
  def btn_a_too_high() -> None:
    data: dict = solution_data.get()
    tab_std_guess.upsert({
      'year': input.num_year(),
      'day': input.num_day(),
      'part': 'A',
      'solution_id': data['run_id_a'],
      'guess': str(data['answer_a']),
      'comparison': 'h'
    })
    ui.notification_show(
      'Guess saved!',
      duration=2,
      type='message'
    )


  @reactive.effect
  @reactive.event(input.btn_b_too_low)
  def btn_b_too_low() -> None:
    data: dict = solution_data.get()
    tab_std_guess.upsert({
      'year': input.num_year(),
      'day': input.num_day(),
      'part': 'B',
      'solution_id': data['run_id_b'],
      'guess': str(data['answer_b']),
      'comparison': 'l'
    })
    ui.notification_show(
      'Guess saved!',
      duration=2,
      type='message'
    )

  @reactive.effect
  @reactive.event(input.btn_b_correct)
  def btn_b_correct() -> None:
    data: dict = solution_data.get()
    tab_std_guess.upsert({
      'year': input.num_year(),
      'day': input.num_day(),
      'part': 'B',
      'solution_id': data['run_id_b'],
      'guess': str(data['answer_b']),
      'comparison': 'c'
    })
    ui.notification_show(
      'Guess saved!',
      duration=2,
      type='message'
    )

  @reactive.effect
  @reactive.event(input.btn_b_too_high)
  def btn_b_too_high() -> None:
    data: dict = solution_data.get()
    tab_std_guess.upsert({
      'year': input.num_year(),
      'day': input.num_day(),
      'part': 'B',
      'solution_id': data['run_id_b'],
      'guess': str(data['answer_b']),
      'comparison': 'h'
    })
    ui.notification_show(
      'Guess saved!',
      duration=2,
      type='message'
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
      'Part B answer was copied to clipboard!',
      type='message',
      duration=2
    )

  @render.data_frame
  def tbl_debug_pre() -> render.DataTable:
    data: dict = debug_logs_pre.get()
    df: pl.DataFrame = pl.DataFrame(
      data=data,
      schema=['data', 'label', 'context']
    )
    return render.DataTable(
      data=df,
      width='100%',
      height='300px',
      filters=True,
      summary=False
    )

  @render.data_frame
  def tbl_debug_a() -> render.DataTable:
    data: dict = debug_logs_a.get()
    df: pl.DataFrame = pl.DataFrame(
      data=data,
      schema=['data', 'label', 'context']
    )
    return render.DataTable(
      data=df,
      width='100%',
      height='300px',
      filters=True,
      summary=False
    )

  @render.data_frame
  def tbl_debug_b() -> render.DataTable:
    data: dict = debug_logs_b.get()
    df: pl.DataFrame = pl.DataFrame(
      data=data,
      schema=['data', 'label', 'context']
    )
    return render.DataTable(
      data=df,
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
      return ui.h2(f'Answer: {"XXXXX" if mask_answer else a_output}')
    return ui.h2('')

  @render.ui
  def txt_a_validation() -> Tag:
    data: dict = solution_data.get()
    a_output: int = int(data.get('answer_a', 0))
    validation: int = int(data.get('expected_a', 0))
    if not data.get('test', False) or not a_output:
      return ui.h4('')
    validation_str: str = ''
    if validation:
      if a_output < validation:
        validation_str = f'Your answer is too low by {validation - a_output}'
      elif a_output == validation:
        validation_str = 'Your answer is correct!'
      else:
        validation_str = f'Your answer is too high by {a_output - validation}!'
    return ui.h4(validation_str)

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
      return ui.h2(f'Answer: {"XXXXX" if mask_answer else b_output}')
    return ui.h2('')

  @render.ui
  def txt_b_validation() -> Tag:
    data: dict = solution_data.get()
    b_output: int = int(data.get('answer_b') or 0)
    validation: int = int(data.get('expected_b') or 0)
    validation_str: str = ''
    if not data.get('test', False) or not b_output:
      return ui.h4('')
    if validation:
      if b_output < validation:
        validation_str = f'Your answer is too low by {validation - b_output}!'
      elif b_output == validation:
        validation_str = 'Your answer is correct!'
      else:
        validation_str = f'Your answer is too high by {b_output - validation}!'
    return ui.h4(validation_str)

  @render.ui
  def txt_b_processing_time() -> Tag:
    data: dict = solution_data.get()
    a_time: float = data.get('b_processing_time')
    if a_time is not None:
      return ui.h4(f'Processing time: {round(a_time, 5)}s')
    return ui.h4('')

  @render.code
  def txt_error_message_pre() -> str:
    return error_message_pre.get()
  
  @render.code
  def txt_error_message_a() -> str:
    return error_message_a.get()

  @render.code
  def txt_error_message_b() -> str:
    return error_message_b.get()
