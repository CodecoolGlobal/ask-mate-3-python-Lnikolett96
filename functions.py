import csv
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg'}
UPLOAD_FOLDER = "./static/images/"

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_data_file(filename):
    data = []
    with open(filename, "r") as file:
        file = csv.reader(file, delimiter=",")
        for row in file:
            data.append(row)
    return data


def write_in_csv(filename, new_data):
    data = get_data_file(filename)
    data.append(new_data)
    with open(filename, "w", newline='') as f:
        file = csv.writer(f, delimiter=",")
        file.writerows(data)


def update_csv(filename, id_num, new_data):
    data = get_data_file(filename)
    index = 0
    for num, row in enumerate(data):
        if row[0] == id_num:
            data.remove(data[num])
            index = num
    data.insert(index, new_data)
    with open(filename, "w", newline='') as f:
        file = csv.writer(f, delimiter=",")
        file.writerows(data)


def make_new_id(filename):
    csv_reader = get_data_file(filename)
    id_num = 0
    if len(csv_reader) == 0:
        id_num = 1
    for row in csv_reader:
        id_num += 1
    return id_num


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


def add_q_a_form(csv_filename, id_num, mode, view_number=0, vote_number=0):
    img_source = save_image('image')
    new_id = ''
    if mode == 'add':
        new_id = make_new_id(csv_filename)
    elif mode == 'update':
        new_id = id_num
    new_data = [new_id, request.form['submission_time'], view_number,
                vote_number, request.form['title'], request.form['message'],
                img_source]
    if mode == 'add':
        write_in_csv(csv_filename, new_data)
    elif 'update':
        update_csv(csv_filename, id_num, new_data)


def load_info_by_csv(csv_filename, id_num):
    data = get_data_file(csv_filename)
    updated_user = []
    for row in data:
        if row[0] == id_num:
            for element in row:
                updated_user.append(element)
    return updated_user






if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
