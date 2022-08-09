from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def main_page(cursor, order_by):
    query = sql.SQL("select * from question order by {pkey}").format(
        pkey=sql.Identifier(order_by))
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def link_with_answer(cursor, id):
    query = """ SELECT * FROM answer WHERE question_id = %(id)s"""
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def del_question(cursor, id):
    query = """
    DELETE FROM
    question WHERE id = %(id)s
    """
    cursor.execute(query, {'id':id})

@database_common.connection_handler
def del_answer(cursor, id):
    query = """
    DELETE FROM
    answer WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})
