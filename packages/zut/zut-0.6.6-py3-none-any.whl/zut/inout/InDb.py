from __future__ import annotations

import logging
from hashlib import sha1

from ..db import create_db_wrapper_with_schema_and_table, DbWrapper
from ..colors import Colors
from .InTable import InTable

logger = logging.getLogger(__name__)


class InDb(InTable):
    def __init__(self, src: str|DbWrapper, query: str = None, params: list|tuple|dict = None, limit: int = None, **kwargs):
        if isinstance(src, DbWrapper):
            self.db = src
            schema = None
            table = None
            super().__init__(self.db.get_uri(with_password=False), **kwargs)
            self._must_exit_db = False
        else:
            super().__init__(src, **kwargs)
            self.db, schema, table = create_db_wrapper_with_schema_and_table(self.src)
            self.name = self.db.get_uri(table=(schema, table), with_password=False)
            self._must_exit_db = True
        

        self._query = query
        self._limit = limit
        self._params = params
        if self._query:
            sha1_prefix = sha1(self._query.encode('utf-8')).hexdigest()[0:8]
            self.name = f"{self.name}#{sha1_prefix}"
        elif table:
            if self._params:
                raise ValueError(f'table query cannot contain params')
            self._query = self.db.get_select_table_query((schema, table))
        else:
            raise ValueError(f'neither a table or a query was given')

        if self._debug:
            logger.debug(f"execute {self.name} with params {self._params}, limit={self._limit}\n{Colors.CYAN}{self._query}{Colors.RESET}")

        # set in __enter__() -> _prepare():
        self._cursor = None


    def _prepare(self):
        self._cursor = self.db.execute_get_cursor(self._query, self._params, limit=self._limit)

        self.headers = self.db.get_cursor_column_names(self._cursor)


    def _get_next_values(self):
        cursor_row = next(self._cursor)
        return list(cursor_row)


    def _end(self):
        self._cursor.close()
        if self._must_exit_db:
            self.db.__exit__()
