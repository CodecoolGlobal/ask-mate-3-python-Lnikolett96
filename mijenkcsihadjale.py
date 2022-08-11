from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

@database_common.connection_handler
def get_img_src(cursor,id):
    cursor.execute(sql.SQL("select image from question where id = %s" % id))
    return cursor.fetchall()

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

@database_common.connection_handler
def add_comment_to_question(cursor, question_id, new_comment):
    cursor.execute(sql.SQL("insert into comment(question_id,message) values (%s, '%s')" % (question_id, new_comment)))

@database_common.connection_handler
def display_comments(cursor, id):
    cursor.execute(sql.SQL("select id, question_id, message, edited_count from comment where question_id=%s" % id))
    return cursor.fetchall()


@database_common.connection_handler
def display_comments_in_answer(cursor, id):
    cursor.execute(sql.SQL("SELECT id, answer_id, message, edited_count FROM comment WHERE answer_id=%s" % id))
    return cursor.fetchall()

@database_common.connection_handler
def delete_comments_from_question(cursor, comment_id):
    cursor.execute(sql.SQL("DELETE FROM comment WHERE id=%s" % comment_id))

@database_common.connection_handler
def main_page_latest_five(cursor):
    query = sql.SQL("select * from question order by submission_time limit 5")
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def question_tag(cursor, question_id):
    cursor.execute(sql.SQL("select name from tag inner join question_tag on tag.id = question_tag.tag_id where question_id=%s" % question_id))
    return cursor.fetchall()

@database_common.connection_handler
def get_new_tag_id(cursor, tag):
    cursor.execute(sql.SQL("SELECT * FROM tag WHERE name=%s" % (tag)))
    return cursor.fetchall()

@database_common.connection_handler
def get_all_tag(cursor):
    cursor.execute(sql.SQL("SELECT name FROM tag"))
    return cursor.fetchall()


@database_common.connection_handler
def add_tag(cursor, question_id, name):
    minden_tag = get_all_tag()
    tagid = get_new_tag_id(name)
    tag_id = tagid[0]['id']
    for element in minden_tag:
        if element['name'] == name:
            cursor.execute(
                sql.SQL("INSERT INTO question_tag(question_id, tag_id) VALUES (%s, %s)" % (question_id, tag_id)))
        else:
            cursor.execute(sql.SQL("INSERT INTO tag(name) VALUES (%s)" % (name)))
            cursor.execute(
                sql.SQL("INSERT INTO question_tag(question_id, tag_id) VALUES (%s, %s)" % (question_id, tag_id)))













