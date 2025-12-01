from os import getcwd, makedirs, path
from shiny import (
  Inputs,
  module,
  Outputs,
  reactive,
  Session,
  ui
)

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
    year: str = str(input.num_input_year())
    day: str = str(input.num_input_day())

    directory: str = path.join(getcwd(), 'solutions', f'Y{year}', 'inputs')
    part_a_test_path: str = path.join(directory, f'{day}-a-test.txt')
    part_b_test_path: str = path.join(directory, f'{day}-b-test.txt')
    day_path: str = path.join(directory, f'{day}.txt')

    ui.update_text_area(
      id='txt_test_a',
      value=open(part_a_test_path, 'r').read() if path.exists(part_a_test_path) else ''
    )
    ui.update_text_area(
      id='txt_test_b',
      value=open(part_b_test_path, 'r').read() if path.exists(part_b_test_path) else ''
    )
    ui.update_text_area(
      id='txt_day_input',
      value=open(day_path, 'r').read() if path.exists(day_path) else ''
    )
  
  @reactive.effect
  @reactive.event(input.btn_save_inputs)
  def btn_save_inputs() -> None:
    year: str = str(input.num_input_year())
    day: str = str(input.num_input_day())

    directory: str = path.join(getcwd(), 'solutions', f'Y{year}', 'inputs')
    part_a_test_path: str = path.join(directory, f'{day}-a-test.txt')
    part_b_test_path: str = path.join(directory, f'{day}-b-test.txt')
    day_path: str = path.join(directory, f'{day}.txt')

    if not path.exists(directory):
      makedirs(directory, exist_ok=True)

    part_a: str = input.txt_test_a()
    part_b: str = input.txt_test_b()
    day_part: str = input.txt_day_input()

    if part_a:
      open(part_a_test_path, 'w').write(part_a)
      ui.notification_show(
        'Part A was updated successfully!',
        duration=2
      )
    if part_b:
      open(part_b_test_path, 'w').write(part_b)
      ui.notification_show(
        'Part B was updated successfully!',
        duration=2
      )
    if day_part:
      open(day_path, 'w').write(day_part)
      ui.notification_show(
        'Day input was updated successfully!',
        duration=2
      )
