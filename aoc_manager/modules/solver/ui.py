from datetime import datetime
from shiny import module, ui
from shiny.ui import Tag


@module.ui
def solver_ui() -> Tag:
  return ui.layout_sidebar(
    ui.sidebar(
      ui.input_numeric(
        id='num_year',
        label='Year',
        value=datetime.now().year,
        min=2020,
        max=datetime.now().year,
        step=1
      ),
      ui.input_numeric(
        id='num_day',
        label='Day',
        value=datetime.now().day,
        min=1,
        max=31,
        step=1
      ),
      ui.input_select(
        id='sel_day_part',
        label='Part',
        choices={'a': 'A', 'b': 'B', 'both': 'Both'},
        selected='both'
      ),
      ui.input_checkbox(
        id='chk_test',
        label='Test',
        value=True
      ),
      ui.input_checkbox(
        id='chk_debug',
        label='Debug',
        value=False
      ),
      ui.input_checkbox(
        id='chk_mask_answers',
        label='Mask Answers',
        value=False
      ),
      ui.input_action_button(
        id='btn_run',
        label='Run',
        class_='btn btn-success'
      )
    ),
    ui.layout_column_wrap(
      ui.card(
        ui.card_header(ui.output_text('txt_day_information')),
        ui.output_ui('txt_total_processing_time'),
        ui.output_ui('txt_preprocessing_time'),
        ui.card(
          ui.card_header('Part A'),
          ui.output_ui('txt_a_output'),
          ui.output_ui('txt_a_validation'),
          ui.output_ui('txt_a_processing_time'),
          ui.input_action_button(
            id='btn_copy_a',
            label='Copy Answer to Clipboard'
          ),
          ui.input_action_button(
            id='btn_save_a',
            label='Save Answer'
          ),
          ui.output_code('txt_error_message_a')
        ),
        ui.card(
          ui.card_header('Part B'),
          ui.output_ui('txt_b_output'),
          ui.output_ui('txt_b_validation'),
          ui.output_ui('txt_b_processing_time'),
          ui.input_action_button(
            id='btn_copy_b',
            label='Copy Answer to Clipboard'
          ),
          ui.input_action_button(
            id='btn_save_b',
            label='Save Answer'
          ),
          ui.output_code('txt_error_message_b')
        ),
        ui.card(
          ui.card_header('Debug Logs'),
          ui.input_numeric(
            id='num_max_logs',
            label='Limit',
            width='20%',
            value=100,
            min=1,
            max=1_000_000,
            step=1
          ),
          ui.output_data_frame('tbl_debug'),
          ui.card_footer(
            ui.input_action_button(
              id='btn_fetch_debug_logs',
              label='Fetch',
              width='45%',
              class_='btn btn-primary'
            )
          )
        )
      )
    )
  )