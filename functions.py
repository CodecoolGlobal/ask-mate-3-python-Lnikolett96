from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import database_common

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


def add_q_a_form():
    img_source = save_image('image')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
