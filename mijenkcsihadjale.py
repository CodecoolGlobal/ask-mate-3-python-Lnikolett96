from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def main_page(cursor,order_by):
    query = sql.SQL("select * from question order by {pkey}").format(
        pkey=sql.Identifier(order_by))
    cursor.execute(query)
    return cursor.fetchall()