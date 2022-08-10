from flask import Flask, render_template, request, redirect, url_for
import database_common
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

UPLOAD_FOLDER = "./static/images/"

app = Flask(__name__)


@database_common.connection_handler
def add_question(cursor, title, message, image) -> list:
    image = save_image("image")
    query = """
    INSERT INTO question(title, message, image)
    VALUES (%(title)s, %(message)s, %(image)s) 
    """
    cursor.execute(query, {'title': title, 'message': message, 'image': image})


@database_common.connection_handler
def add_answer(cursor, question_id, message, image) -> list:
    image = save_image("image")
    query = """
    INSERT INTO answer(question_id, message, image)
    VALUES (%(question_id)s, %(message)s, %(image)s)
    """
    cursor.execute(query, {'question_id': question_id, 'message': message, 'image': image})


def save_image(file_name_in_form):
    uploaded_file = request.files[file_name_in_form]
    img_source = ""
    if uploaded_file.filename != '':
        uploaded_file.save(UPLOAD_FOLDER + uploaded_file.filename)
        img_source = UPLOAD_FOLDER + uploaded_file.filename
    return img_source


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
def get_question(cursor: RealDictCursor, id) -> list:
    query = """
    SELECT *  FROM question WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@database_common.connection_handler
def search_question(cursor: RealDictCursor, search) -> list:
    search = '%' + search + '%'
    query = sql.SQL("SELECT * FROM question WHERE title LIKE %(search)s OR message LIKE %(search)s")
    cursor.execute(query, {'search': search})
    return cursor.fetchall()


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
