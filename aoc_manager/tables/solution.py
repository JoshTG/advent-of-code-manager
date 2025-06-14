from deltalake import Field, Schema
from polta.enums import TableQuality
from polta.table import PoltaTable

from tools.metastore import metastore


table: PoltaTable = PoltaTable(
  domain='aoc',
  quality=TableQuality.CANONICAL,
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
