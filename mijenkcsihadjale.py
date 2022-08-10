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
def vote_up(cursor, id):
    query = """
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id':id})

@database_common.connection_handler
def del_answer(cursor, id):
    query = """
    DELETE FROM
    answer WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})

@database_common.connection_handler
def vote_down(cursor, id):
    query = """
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id':id})

@database_common.connection_handler
def answer_vote_down(cursor, id):
    query = """
    UPDATE answer
    SET vote_number = vote_number - 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id':id})

@database_common.connection_handler
def answer_vote_up(cursor, id):
    query = """
    UPDATE answer
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id':id})

@database_common.connection_handler
def add_comment_to_answer(cursor, answer_id, new_message):
    cursor.execute(sql.SQL("insert into comment(answer_id,message) values (%s, '%s')" % (answer_id,new_message)))

@database_common.connection_handler
def get_question_id(cursor, answer_id):
    cursor.execute(sql.SQL("select question_id from answer where id=%s" % answer_id))
    return cursor.fetchall()
