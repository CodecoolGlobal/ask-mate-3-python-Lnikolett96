from flask import Flask, render_template, request, redirect, url_for
import database_common
from psycopg2.extras import RealDictCursor

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

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
