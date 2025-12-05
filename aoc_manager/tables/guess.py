from deltalake import Field, Schema
from polta.table import Table, TableQuality

from aoc_manager.tools.metastore import metastore


table: Table = Table(
  domain='aoc',
  quality=TableQuality.STANDARD,
  name='guess',
  raw_schema=Schema([
    Field('year', 'integer'),
    Field('day', 'integer'),
    Field('part', 'string'),
    Field('solution_id', 'string'),
    Field('guess', 'string'),
    Field('comparison', 'string')
  ]),
  primary_keys=['year', 'day', 'part', 'guess'],
  metastore=metastore
)
