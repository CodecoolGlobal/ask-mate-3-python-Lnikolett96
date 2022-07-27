from flask import Flask, render_template, redirect, url_for, request
import csv
from valami import write_in_csv

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def hello():
    ranking = True
    questions = []
    with open("./sample_data/question.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            questions.append(row)

    ordering_list = []
    ordered_by = request.args.get("ordered_by", "title")
    order_direction = request.args.get("order_direction", "desc")
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

    return render_template('main_page.html', questions_again=questions_again, questions = questions)



@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    add = True
    title = 'Add Question'
    if request.method == 'POST':
        return redirect(url_for('main_page.html'))
    return render_template('add.html', add=add, title=title)

@app.route('/delete')
def delete_page():
    return render_template('delete_page.html')

@app.route('/question/<question_id>/delete',methods = ['GET','POST'])
def delete_question(question_id):

    questions = []
    with open("./sample_data/question.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            questions.append(row)
    for index in range(len(questions)):
        if questions[index]['id'] == str(question_id):
            del questions[index]
            print(questions)
            break



    with open("./sample_data/question.csv",'w', newline='') as file:
        fieldnames = ["id","submission_time","view_number","vote_number","title", "message","image","delete"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for dict in questions:
            writer.writerow(dict)


    return redirect('/')

@app.route('/question/<answer_id>/delete',methods = ['GET','POST'])
def delete_answer(answer_id):

    answers = []
    with open("./sample_data/answer.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            answers.append(row)
    for index in range(len(answers)):
        if answers[index]['id'] == str(answer_id):
            del answers[index]
            print(answers)
            break



    with open("./sample_data/answer.csv",'w', newline='') as file:
        fieldnames = ["id","submission_time","view_number","vote_number","title", "message","image","delete"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for dict in answers:
            writer.writerow(dict)


    return redirect('/')




if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
