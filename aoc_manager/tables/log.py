from deltalake import Field, Schema
from polta.table import Table, TableQuality

from aoc_manager.tools.metastore import metastore


table: Table = Table(
  domain='aoc',
  quality=TableQuality.STANDARD,
  name='log',
  raw_schema=Schema([
    Field('year', 'integer'),
    Field('day', 'integer'),
    Field('context', 'string'),
    Field('data', 'string'),
    Field('label', 'string')
  ]),
  primary_keys=['year', 'day'],
  metastore=metastore
)
