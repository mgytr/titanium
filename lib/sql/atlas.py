import inspect

from atlas_provider_sqlalchemy.ddl import print_ddl

from . import sql

print_ddl(
    "postgresql",
    [table[1] for table in inspect.getmembers(sql) if hasattr(table[1], "__tablename__")],
)
