from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

UPLOAD_FOLDER = "./static/images/"

app = Flask(__name__)


def current_time():
    now = datetime.now()
    time_current = now.strftime("%H:%M:%S")
    return time_current


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
