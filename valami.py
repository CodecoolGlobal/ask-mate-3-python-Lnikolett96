import csv

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


def get_data_file(filename):
    data = []
    with open(filename, "r") as file:
        file = csv.reader(file, delimiter=",")
        for row in file:
            data.append(row)
    return data


def write_in_csv(filename, new_data):
    with open(filename, "w") as f:
        file = csv.writer(f, delimiter=",")
        for elem in new_data:
            file.writerow(elem)


def make_new_id(new_data):
    max_id = 0
    for elem in new_data:
        elem = int(elem)
        if elem > max_id:
            max_id = elem
    return max_id + 1


def current_time():
    now = datetime.now()
    time_current = now.strftime("%H:%M:%S")
    return time_current


def add_q_a_form(filename):
    view_number = 0
    vote_number = 0
    image = ""
    if request.form['image'] == "":
        image = None
    else:
        image = request.form['image']

    records = get_data_file(filename)
    new_id = make_new_id(records[1:])
    new_data = [new_id, request.form['submission_time'], view_number,
                vote_number, request.form['title'], request.form['message'],
                image]
    write_in_csv(filename, new_data)
    return


@app.route('/')
def alap():
    return 'Ez már Valami'


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    add = True
    title = 'Add Question'
    time = current_time()
    if request.method == 'POST':
        add_q_a_form("/sample_data/question.csv")
        return redirect(url_for('alap'))
    return render_template('add.html', add=add, title=title, time=time)


@app.route('/update-question', methods=['GET', 'POST'])
def update_question(id):
    add = False
    # if request.method == 'GET':
    file = get_data_file('./sample_data/question.csv')
    for row in file:
        if row[0] == id:
            return render_template('add.html', row=row, add=add)
    return render_template('add.html', row=None, add=add)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
