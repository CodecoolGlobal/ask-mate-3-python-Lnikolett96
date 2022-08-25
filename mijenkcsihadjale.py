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
def vote_up(cursor, id, user_id):
    query = """
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    query1 = """
        UPDATE users
        SET reputation = reputation + 5
        WHERE id = %(user_id)s
        """
    cursor.execute(query, {'id':id})
    cursor.execute(query1, {'user_id': user_id})

@database_common.connection_handler
def del_answer(cursor, id):
    query = """
    DELETE FROM
    answer WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})

@database_common.connection_handler
def vote_down(cursor, id, user_id):
    query = """
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id = %(id)s
    """
    query1 = """
            UPDATE users
            SET reputation = reputation - 2
            WHERE id = %(user_id)s
            """
    cursor.execute(query1, {'user_id': user_id})
    cursor.execute(query, {'id':id})

@database_common.connection_handler
def answer_vote_down(cursor, id, user_id):
    query = """
    UPDATE answer
    SET vote_number = vote_number - 1
    WHERE id = %(id)s
    """
    query1 = """
                UPDATE users
                SET reputation = reputation - 2
                WHERE id = %(user_id)s
                """
    cursor.execute(query1, {'user_id': user_id})
    cursor.execute(query, {'id':id})

@database_common.connection_handler
def answer_vote_up(cursor, id, user_id):
    query = """
    UPDATE answer
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    query1 = """
            UPDATE users
            SET reputation = reputation + 10
            WHERE id = %(user_id)s
            """
    cursor.execute(query, {'id':id})
    cursor.execute(query1, {'user_id': user_id})

@database_common.connection_handler
def add_comment_to_answer(cursor, answer_id, new_message, user_id):
    cursor.execute(sql.SQL("insert into comment(answer_id,message, user_id) values (%s, '%s', %s)" % (answer_id,new_message, user_id)))

@database_common.connection_handler
def get_question_id(cursor, answer_id):
    cursor.execute(sql.SQL("select question_id from answer where id=%s" % answer_id))
    return cursor.fetchall()

@database_common.connection_handler
def add_comment_to_question(cursor, question_id, new_comment, user_id):
    cursor.execute(sql.SQL("insert into comment(question_id,message, user_id) values (%s, '%s', %s)" % (question_id, new_comment, user_id)))

@database_common.connection_handler
def display_comments(cursor, id):
    cursor.execute(sql.SQL("select id, question_id, message, edited_count, user_id from comment where question_id=%s" % id))
    return cursor.fetchall()


@database_common.connection_handler
def display_comments_in_answer(cursor, id):
    cursor.execute(sql.SQL("SELECT id, answer_id, message, edited_count, user_id FROM comment WHERE answer_id=%s" % id))
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
    cursor.execute("SELECT * FROM tag WHERE name=%(tag)s", {'tag':tag})
    return cursor.fetchall()

@database_common.connection_handler
def get_all_tag(cursor):
    cursor.execute(sql.SQL("SELECT name FROM tag"))
    return cursor.fetchall()

@database_common.connection_handler
def user_page_answer(cursor, user_id):
    cursor.execute("SELECT * FROM answer WHERE user_id = %(user_id)s", {'user_id': user_id})
    return cursor.fetchall()

@database_common.connection_handler
def user_page_question(cursor, user_id):
    cursor.execute("SELECT * FROM question WHERE user_id = %(user_id)s", {'user_id': user_id})
    return cursor.fetchall()

@database_common.connection_handler
def user_page_comment(cursor, user_id):
    cursor.execute("SELECT * FROM comment WHERE user_id = %(user_id)s", {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def register(cursor, user, password, email):
    cursor.execute('INSERT INTO users(username, user_password, email) VALUES (%(user)s, %(password)s, %(email)s)', {'user': user, 'password':password, 'email':email})


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
            cursor.execute("INSERT INTO tag(name) VALUES (%(name)s)", {'name': name})
            cursor.execute(
                sql.SQL("INSERT INTO question_tag(question_id, tag_id) VALUES (%s, %s)" % (question_id, tag_id)))

@database_common.connection_handler
def get_reputation(cursor, user_id):
    cursor.execute("SELECT reputation FROM users where id = %(user_id)s", {'user_id': user_id})
    return cursor.fetchone()

@database_common.connection_handler
def get_user_id(cursor, question_id):
    cursor.execute("SELECT user_id FROM question where id = %(question_id)s", {'question_id': question_id})
    return cursor.fetchone()

@database_common.connection_handler
def get_user_id_by_answer(cursor, answer_id):
    cursor.execute("SELECT user_id FROM answer where id = %(answer_id)s", {'question_id': answer_id})
    return cursor.fetchone()









