from deltalake import Field, Schema
from polta.table import Table, TableQuality

from aoc_manager.tools.metastore import metastore


table: Table = Table(
  domain='aoc',
  quality=TableQuality.STANDARD,
  name='input',
  raw_schema=Schema([
    Field('year', 'integer'),
    Field('day', 'integer'),
    Field('input_test_a', 'string'),
    Field('expected_a', 'string'),
    Field('input_test_b', 'string'),
    Field('expected_b', 'string'),
    Field('full_input', 'string')
  ]),
  primary_keys=['year', 'day'],
  metastore=metastore
)
