from os import getcwd, makedirs, path
from shiny import (
  Inputs,
  module,
  Outputs,
  reactive,
  Session,
  ui
)
from typing import Any

from aoc_manager.tables.input import \
  table as tab_aoc_input
from aoc_manager.tools.solver_template import solver_template


@module.server
def inputs_server(input: Inputs, output: Outputs, session: Session) -> None:
  @reactive.effect
  @reactive.event(input.btn_create_new_solver)
  def btn_create_new_solver() -> None:
    year: str = str(input.num_input_year())
    day: str = str(input.num_input_day())

    directory: str = path.join(getcwd(), 'solutions', f'Y{year}', 'solutions')
    file_path: str = path.join(directory, f'd{day}.py')

    if path.exists(file_path):
      ui.notification_show(
        'Warning: Solver already exists for that day.',
        type='warning',
        duration=3
      )
    else:
      if not path.exists(directory):
        makedirs(directory, exist_ok=True)

      open(file_path, 'w').write(solver_template.format(day=day))
      ui.notification_show(
        'Success! Your solver has been created.',
        type='message',
        duration=2
      )

  @reactive.effect
  @reactive.event(input.btn_load_inputs)
  def btn_load_inputs() -> None:
    rows: list[dict] = tab_aoc_input.get(
      filter_conditions={
        'year': input.num_input_year(),
        'day': input.num_input_day()
      },
    ).to_dicts()

    if not rows:
      ui.notification_show(
        'No inputs found for this day.',
        duration=3,
        type='warning'
      )
      return

    row: dict[str, Any] = rows[0]

    ui.update_text_area(
      id='txt_test_a',
      value=row['input_test_a']
    )
    ui.update_text_area(
      id='txt_test_a_solution',
      value=row['expected_a']
    )
    ui.update_text_area(
      id='txt_test_b',
      value=row['input_test_b']
    )
    ui.update_text_area(
      id='txt_test_b_solution',
      value=row['expected_b']
    )
    ui.update_text_area(
      id='txt_day_input',
      value=row['full_input']
    )
  
  @reactive.effect
  @reactive.event(input.btn_save_inputs)
  def btn_save_inputs() -> None:
    payload: dict[str, Any] = {
      'year': input.num_input_year(),
      'day': input.num_input_day(),
      'input_test_a': input.txt_test_a(),
      'expected_a': input.txt_test_a_solution(),
      'input_test_b': input.txt_test_b(),
      'expected_b': input.txt_test_b_solution(),
      'full_input': input.txt_day_input()
    }
    tab_aoc_input.upsert(payload)

    ui.notification_show(
      'Input was saved successfully!',
      duration=3,
      type='message'
    )
