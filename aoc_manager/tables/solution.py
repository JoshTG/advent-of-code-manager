from deltalake import Field, Schema
from polta.table import Table, TableQuality

from aoc_manager.tools.metastore import metastore


table: Table = Table(
  domain='aoc',
  quality=TableQuality.STANDARD,
  name='solution',
  raw_schema=Schema([
    Field('_execution_ts', 'timestamp'),
    Field('id', 'string'),
    Field('year', 'integer'),
    Field('day', 'integer'),
    Field('part', 'string'),
    Field('test_ind', 'boolean'),
    Field('answer', 'string'),
    Field('processing_time', 'float')
  ]),
  metastore=metastore
)
