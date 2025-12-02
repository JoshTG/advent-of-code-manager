import polars as pl

from shiny import (
  Inputs,
  module,
  Outputs,
  reactive,
  render,
  Session
)
from shiny.reactive import Value

from aoc_manager.tables.answer import table as pt_can_answer

answer_cols: list[str] = ['year', 'day', 'part', 'test_ind', 'answer']
solutions: Value = Value(pt_can_answer.get(select=answer_cols))

@module.server
def solutions_server(input: Inputs, output: Outputs, session: Session) -> None:
  @reactive.effect
  @reactive.event(input.btn_refresh_solutions)
  def btn_refresh_solutions():
    solutions.set(pt_can_answer.get(select=answer_cols))

  @render.data_frame
  def tbl_solutions():
    df: pl.DataFrame = solutions.get()

    df: pl.DataFrame = df \
      .select(
        pl.col('year').alias('Year'),
        pl.col('day').alias('Day'),
        pl.concat_str(
          pl.col('part').str.to_uppercase(),
          pl.lit(' '), 
          pl.when('test_ind').then(pl.lit('Test')).otherwise(pl.lit(''))
        ).alias('Part'),
        pl.col('answer').alias('Answer')
      ) \
      .pivot(
        ['Part'],
        index=['Year', 'Day'],
        values='Answer'
      ) \
      .sort('Year', 'Day')
    return render.DataTable(
      data=df,
      width='100%',
      height='600px',
      summary=False,
      filters=True
    )
