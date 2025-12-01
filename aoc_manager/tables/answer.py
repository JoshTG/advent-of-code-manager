from deltalake import Field, Schema
from polta.table import Table, TableQuality

from aoc_manager.tools.metastore import metastore


table: Table = Table(
  domain='aoc',
  quality=TableQuality.STANDARD,
  name='answer',
  raw_schema=Schema([
    Field('year', 'integer'),
    Field('day', 'integer'),
    Field('part', 'string'),
    Field('test_ind', 'boolean'),
    Field('solution_id', 'string'),
    Field('answer', 'string')
  ]),
  primary_keys=['year', 'day', 'part', 'test_ind'],
  metastore=metastore
)
