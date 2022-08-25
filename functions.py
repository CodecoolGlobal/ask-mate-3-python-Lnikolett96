from flask import Flask, render_template, request, redirect, url_for
import database_common
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

UPLOAD_FOLDER = './static/images/'


@database_common.connection_handler
def add_question(cursor, title, message, image, user_id) -> list:
    image = save_image("image")
    query = """
    INSERT INTO question(title, message, image,user_id)
    VALUES (%(title)s, %(message)s, %(image)s, %(user_id)s) 
    """
    cursor.execute(query, {'title': title, 'message': message, 'image': image, 'user_id': user_id})


@database_common.connection_handler
def add_answer(cursor, question_id, message, image, user_id) -> list:
    image = save_image("image")
    query = """
    INSERT INTO answer(question_id, message, image, user_id)
    VALUES (%(question_id)s, %(message)s, %(image)s, %(user_id)s)
    """
    cursor.execute(query, {'question_id': question_id, 'message': message, 'image': image, 'user_id':user_id})


def save_image(file_name_in_form):
    uploaded_file = request.files[file_name_in_form]
    if uploaded_file.filename != '':
        uploaded_file.save(UPLOAD_FOLDER + uploaded_file.filename)
        upload_fold ="/static/images/"
        image_source = upload_fold + uploaded_file.filename
        return image_source
    else:
        return None


@database_common.connection_handler
def update_question(cursor, id_num, title, message, image) -> list:
    image = save_image("image")
    query = """
        UPDATE question 
        SET title = %(title)s, message = %(message)s, image = %(image)s
        WHERE id = %(id_num)s
    """
    cursor.execute(query, {'id_num': id_num, 'title': title, 'message': message, 'image': image})


@database_common.connection_handler
def update_answer(cursor, id_num, message, image='not'):
    image = save_image("image")
    query = """
            UPDATE answer 
            SET  message = %(message)s, image = %(image)s
            WHERE id = %(id_num)s
        """
    cursor.execute(query, {'id_num': id_num, 'message': message, 'image': image})


@database_common.connection_handler
def update_comment(cursor, id, message):
    query = """
                UPDATE comment 
                SET  message = %(message)s, edited_count += 1
                WHERE id = %(id)s
            """
    cursor.execute(query, {'id': id, 'message': message})

@database_common.connection_handler
def get_question(cursor: RealDictCursor, id) -> list:
    query = """
    SELECT *  FROM question WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def get_comment(cursor: RealDictCursor, id) -> list:
    query = """
        SELECT *  FROM comment WHERE id = %(id)s
        """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def get_answer(cursor: RealDictCursor, id) -> list:
    query = """
        SELECT *  FROM answer WHERE id = %(id)s
        """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@database_common.connection_handler
def search_question(cursor: RealDictCursor, search) -> list:
    search = '%' + search + '%'
    query = sql.SQL("SELECT * FROM question WHERE title LIKE %(search)s OR message LIKE %(search)s")
    cursor.execute(query, {'search': search})
    return cursor.fetchall()


@database_common.connection_handler
def get_users(cursor: RealDictCursor) -> list:
    query = """
        SELECT id, username, email FROM users;
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def check_exist_user_by_username(cursor, username) -> list:
    query = """     
    SELECT * FROM users 
    WHERE username = %(username)s     
    """
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


@database_common.connection_handler
def get_user_id_for_this_question(cursor, id):
    query = """
    SELECT user_id FROM question where id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def check_if_accepted(cursor, id) -> list:
    query = """
    SELECT answer.accepted 
    FROM question
    INNER JOIN answer ON question.id = answer.question_id
    WHERE question_id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()

@database_common.connection_handler
def accepting_answer(cursor, id) -> dict:
    query = """
    UPDATE answer 
    SET accepted = TRUE
    WHERE id = %(id)s
    RETURNING question_id
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@database_common.connection_handler
def get_tags(cursor) -> list:
    query = """
    SELECT name, COUNT(qt.question_id) AS question
    FROM tag
    INNER JOIN question_tag qt ON tag.id = qt.tag_id
    GROUP BY name
    """
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )


