from __future__ import annotations
from io import StringIO
import logging

from ..db import create_db_wrapper_with_schema_and_table
from .OutCsv import OutCsv

logger = logging.getLogger(__name__)


class OutDb(OutCsv):
    def __init__(self, out: str, decimal_separator: str = None, **kwargs):
        # Prepare arguments for base classes (OutCsv, OutTable, OutFile)
        if not isinstance(out, str):
            raise ValueError(f"OutDb's out must be a str, got {type(out).__name__}: {out}")
    
        decimal_separator = '.'
        
        # Initialize base classes (OutCsv, OutTable, OutFile)
        super().__init__(StringIO(), decimal_separator=decimal_separator, **kwargs)

        # Modify attributes set by base classes (OutCsv, OutTable, OutFile)
        self.db, self.schema_name, self.table_name = create_db_wrapper_with_schema_and_table(out.format(**kwargs))
        if not self.table_name:
            raise ValueError(f"invalid db target: table name not provided")
        
        self.name = self.db.get_uri(table=(self.schema_name, self.table_name), with_password=False)

    # -------------------------------------------------------------------------
    # OutFile subclassing
    #

    def _open_file(self):
        existing_headers = super()._open_file()

        # Create, drop or truncate table
        if not self._append:
            logger.debug(f"truncate table %s.%s", self.schema_name, self.table_name)
            self.db.truncate_table((self.schema_name, self.table_name))

        return existing_headers
                

    def _close_file(self):
        if not self._headers:
            if self._row_count == 0:
                return
            raise ValueError(f"cannot export rows to database: no headers")
                
        logger.debug(f"copy data to table %s.%s", self.schema_name, self.table_name)
        self.out.seek(0)
        self.db.copy_from_csv(self.out, (self.schema_name, self.table_name), columns=self._headers, delimiter=self._delimiter, quotechar=self._quotechar)
        self.db.__exit__()


    # -------------------------------------------------------------------------
    # OutTable subclassing
    #
    
    def _get_existing_headers(self) -> list[str]|None:
        # Only export given headers, but check that they are in the target table
        column_names = self.db.get_table_column_names((self.schema_name, self.table_name))
        if not self._headers:
            raise ValueError(f'headers must be set')
        
        missing_columns = []
        for header in self._headers:
            if not header in column_names:
                missing_columns.append(header)

        if missing_columns:
            raise ValueError(f"column not found in out table: {', '.join(missing_columns)}")

        return []
