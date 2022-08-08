from flask import Flask, render_template, redirect, url_for, request
import csv
import functions

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
    time = functions.current_time()
    id_num = functions.make_new_id("./sample_data/question.csv")
    if request.method == 'POST':
        functions.add_q_a_form("./sample_data/question.csv", id_num,'add', 0, 0)
        return redirect('/')
    return render_template('add.html', add=add, title_name=title, time=time)

@app.route('/update-question/<id_num>', methods=['GET', 'POST'])
def update_question(id_num):
    add = False
    update = True
    title_name = 'Update Question'
    time = functions.current_time()
    updated_user = functions.load_info_by_csv("./sample_data/question.csv", id_num)
    view_number = updated_user[2]
    vote_number = updated_user[3]
    if request.method == 'POST':
        functions.add_q_a_form("./sample_data/question.csv", id_num, 'update', view_number, vote_number)
        return redirect('/')
    return render_template('add.html', add=add, update=update, title_name=title_name, time=time,
                           id_num=updated_user[0], submission_time=time, view_number=view_number,
                           vote_number=vote_number, title=updated_user[4], message=updated_user[5])

@app.route('/delete')
def delete_page():
    return render_template('delete_page.html')


@app.route('/question/<question_id>')
def display_question_and_answer(question_id):
    questions = []
    with open("./sample_data/answer.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            questions.append(row)
    answers = []
    print(answers)
    print(questions)
    for dicts in questions:
        if dicts["question_id"] == question_id:
            answers.append(dicts)

    return render_template('question_with_answer.html',questions_again = answers)


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
        fieldnames = ["id","submission_time","view_number","vote_number","title", "message","image","functions"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for dict in questions:
            writer.writerow(dict)


    return redirect('/')

@app.route('/answer/<answer_id>/delete',methods = ['GET','POST'])
def delete_answer(answer_id):
    answers = []
    with open("./sample_data/answer.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            answers.append(row)
    question_id = answers[0]["question_id"]
    for index in range(len(answers)):

        if answers[index]['id'] == str(answer_id):
            del answers[index]
            print(answers)
            break



    with open("./sample_data/answer.csv",'w', newline='') as file:
        fieldnames = ["id","submission_time","question_id","vote_number","message","image","functions"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for dict in answers:
            writer.writerow(dict)


    return redirect(f'/question/{question_id}')

@app.route("/question/<question_id>/vote-up", methods = ['POST','GET'])
def voteup(question_id):
    questions = []
    with open("./sample_data/question.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            questions.append(row)

    for dicts in questions:
        if dicts['id'] == question_id:
            dicts['vote_number'] = int(dicts.get('vote_number',0)) + 1


    with open("./sample_data/question.csv",'w', newline='') as file:
        fieldnames = ["id","submission_time","view_number","vote_number","title", "message","image","functions"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for dict in questions:
            writer.writerow(dict)

    return redirect('/')

@app.route("/question/<question_id>/vote-down", methods = ['POST','GET'])
def votedown(question_id):
    questions = []
    with open("./sample_data/question.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            questions.append(row)

    for dicts in questions:
        if dicts['id'] == question_id:
            dicts['vote_number'] = int(dicts.get('vote_number',0)) - 1


    with open("./sample_data/question.csv",'w', newline='') as file:
        fieldnames = ["id","submission_time","view_number","vote_number","title", "message","image","functions"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for dict in questions:
            writer.writerow(dict)

    return redirect('/')

@app.route("/answer/<answer_id>/vote-up", methods = ["GET", "POST"])
def answer_vote_up(answer_id):
    answer = []
    with open("./sample_data/answer.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            answer.append(row)
    question_id = answer[0]["question_id"]

    for dicts in answer:
        if dicts['id'] == answer_id:
            dicts['vote_number'] = int(dicts.get('vote_number',0)) + 1


    with open("./sample_data/answer.csv",'w', newline='') as file:
        fieldnames = ["id","submission_time","question_id","vote_number","message","image","functions"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for dict in answer:
            writer.writerow(dict)

    return redirect(f"/question/{question_id}")

@app.route("/answer/<answer_id>/vote-down", methods = ['POST','GET'])
def answer_vote_down(answer_id):
    answer = []
    with open("./sample_data/answer.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            answer.append(row)
    question_id = answer[0]["question_id"]

    for dicts in answer:
        if dicts['id'] == answer_id:
            dicts['vote_number'] = int(dicts.get('vote_number',0)) - 1


    with open("./sample_data/answer.csv",'w', newline='') as file:
        fieldnames = ["id","submission_time","question_id","vote_number","message","image","functions"]
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        for dict in answer:
            writer.writerow(dict)

    return redirect(f"/question/{question_id}")

@app.route('/answer/<question_id>/new-answer', methods=['POST', 'GET'])
def answer_questions(question_id):
    answer_data = []
    add = True
    title = 'Add New Answer'
    time = functions.current_time()
    id_num = functions.make_new_id("./sample_data/answer.csv")
    if request.method == 'POST':
        functions.add_q_a_form("./sample_data/answer.csv", id_num, 0, 0, 'add')

        answer_data['new_answer'] = request.form['new_answer']

        return redirect(f"/answer/{question_id}")

    return render_template('new_answer.html', add=add, title_name=title, time=time, question_id=question_id)

@app.route('/added-answer/<question_id>', methods=['POST'])
def add_new_answer(question_id):
    id_num = functions.make_new_id("./sample_data/answer.csv")
    if request.method == 'POST':
        functions.add_q_a_form("./sample_data/answer.csv", id_num, question_id, 0, 'add')

        return redirect('/')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
