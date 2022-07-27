from flask import Flask, render_template, redirect, url_for, request
import csv

app = Flask(__name__)


@app.route("/list")
def hello():
    ranking = True
    questions = []
    with open("./sample_data/question.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            questions.append(row)

    ordering_list = []
    ordered_by = request.args["ordered_by"]
    order_direction = request.args["order_direction"]
    if order_direction == "asc":
        ranking = False
    else:
        ranking = True

    for i in questions:
        if i[ordered_by].isnumeric():
            ordering_list.append(int(i[ordered_by]))
        else:
            ordering_list.append(i[ordered_by])
    ordered_lst = sorted(ordering_list, reverse=ranking)

    questions_again = []
    for i in ordered_lst:
        for k in questions:
            if str(i) == k[ordered_by]:
                questions_again.append(k)

    print(questions_again)

    return render_template('main_page.html', questions_again=questions_again, questions = questions)



@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    add = True
    title = 'Add Question'
    if request.method == 'POST':
        return redirect(url_for('main_page.html'))
    return render_template('add.html', add=add, title=title)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
