from datetime import datetime
from shiny import module, ui
from shiny.ui import Tag


# Variables pertaining to user time
this_year: int = datetime.now().year
today: int = datetime.now().day
max_day: int = 31 if this_year < 2025 else 12

@module.ui
def inputs_ui() -> Tag:
  return ui.layout_sidebar(
    ui.sidebar(
      ui.input_numeric(
        id='num_input_year',
        label='Year',
        value=this_year,
        min=2020,
        max=this_year,
        step=1
      ),
      ui.input_numeric(
        id='num_input_day',
        label='Day',
        value=today,
        min=1,
        max=max_day,
        step=1
      ),
      ui.input_action_button(
        id='btn_create_new_solver',
        label='Create New Solver'
      ),
      ui.input_action_button(
        id='btn_load_inputs',
        label='Load Inputs'
      ),
      ui.input_action_button(
        id='btn_save_inputs',
        label='Save Inputs'
      )
    ),
    ui.card(
      ui.input_text_area(
        id='txt_test_a',
        label='Part A Test',
        width='50%',
        height='200px'
      ),
      ui.input_text(
        id='txt_test_a_solution',
        label='Part A Expected Solution'
      ),
      ui.input_text_area(
        id='txt_day_input',
        label='Day Input',
        width='50%',
        height='200px'
      ),
      ui.input_text_area(
        id='txt_test_b',
        label='Part B Test',
        width='50%',
        height='200px',
        placeholder='Leave empty to default to Part A Test'
      ),
      ui.input_text(
        id='txt_test_b_solution',
        label='Part B Expected Solution'
      ),
    )
  )