import csv
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
import urllib.request
import os

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
    new_data[0] = id
    data[int(id_num)] = new_data
    data.append(new_data)
    with open(filename, "w", newline='') as f:
        file = csv.writer(f, delimiter=",")
        file.writerows(data)


def make_new_id(filename):
    csv_reader = get_data_file(filename)
    id_num = 0
    if not csv_reader:
        id_num = 1
    else:
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


def add_q_a_form(csv_filename, view_number, vote_number):
    img_source = save_image('image')
    new_id = make_new_id(csv_filename)
    new_data = [new_id, request.form['submission_time'], view_number,
                vote_number, request.form['title'], request.form['message'],
                img_source]
    write_in_csv(csv_filename, new_data)
    return


def load_info_by_csv(csv_filename):
    data = get_data_file(csv_filename)
    time = data[1]
    view_number = data[2]
    vote_number = data[3]
    id_num = data[0]
    title = data[4]
    message = data[5]
    return [id_num, time, view_number, vote_number, title, message]


@app.route('/')
def alap():
    return 'Ez már Valami'


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    add = True
    update = False
    title = 'Add Question'
    time = current_time()
    if request.method == 'POST':
        add_q_a_form("./sample_data/question.csv", 0, 0)
        return redirect(url_for('alap'))
    return render_template('add.html', add=add, title_name=title, time=time)


@app.route('/update-question/<id_num>', methods=['GET', 'POST'])
def update_question(id_num):
    add = False
    update = True
    title_name = 'Update Question'
    time = current_time()
    data = load_info_by_csv("./sample_data/question.csv")
    if request.method == 'POST':


        return redirect(url_for('alap'))
    return render_template('add.html', add=add, update=update, title_name=title_name, time=time,
                           idnum=data[0], submission_time=time, view_number=data[2],
                           vote_number=data[3], title=data[4], message=data[5])


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
