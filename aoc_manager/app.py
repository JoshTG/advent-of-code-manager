from locale import LC_ALL, setlocale
from shiny import (
  App,
  Inputs,
  Outputs,
  Session,
  ui
)
from shiny.ui import Tag

from aoc_manager.modules.inputs.server import inputs_server
from aoc_manager.modules.inputs.ui import inputs_ui
from aoc_manager.modules.solutions.server import solutions_server
from aoc_manager.modules.solutions.ui import solutions_ui
from aoc_manager.modules.solver.server import solver_server
from aoc_manager.modules.solver.ui import solver_ui


# Set module-level variables
setlocale(LC_ALL, '')

# Define main app UI and its navbar panels
app_ui: Tag = ui.page_fluid(
  ui.navset_bar(
    ui.nav_panel('Solver',
      solver_ui('solver')
    ),
    ui.nav_panel('Inputs',
      inputs_ui('inputs')
    ),
    ui.nav_panel('Solutions',
      solutions_ui('solutions')
    ),
    title='Advent of Code'
  )
)


# Define main server which contains modules of each navbar panel
def server(input: Inputs, output: Outputs, session: Session):
  solver_server('solver')
  inputs_server('inputs')
  solutions_server('solutions')


# Instantiate the Shiny App
app: App = App(app_ui, server)
