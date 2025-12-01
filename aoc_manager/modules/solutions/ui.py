from shiny import module, ui
from shiny.ui import Tag


@module.ui
def solutions_ui() -> Tag:
  return ui.card( 
    ui.output_data_frame('tbl_solutions'),
    ui.card_footer(
      ui.input_action_button(
        id='btn_refresh_solutions',
        label='Refresh',
        class_='btn btn-success'
      )
    )
  )
