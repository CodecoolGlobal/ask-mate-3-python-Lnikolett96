from flask import Flask, render_template, redirect, url_for, request
import functions
import mijenkcsihadjale

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def hello():
    order_by = request.args.get('ordering', 'id')
    questions = mijenkcsihadjale.main_page(order_by)
    return render_template('main_page.html', questions = questions)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    add = True
    title = 'Add Question'
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        functions.add_question(title, message, image)
        # functions_data_manager, database_common
        return redirect('/')
    return render_template('add.html', add=add, title_name=title)


@app.route('/update-question/<id_num>', methods=['GET', 'POST'])
def get_update_question(id_num):
    title_name = 'Update Question'
    question = functions.get_question(id_num)
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.form.get('image')
        functions.update_question(id_num, title, message, image)
        return redirect('/')
    return render_template('add.html', question=question, id_num=id_num,
                           add=False,
                           title_name=title_name)

@app.route('/delete/<question_id>')
def delete_page(question_id):
    mijenkcsihadjale.del_question(question_id)
    return redirect('/')


@app.route('/question/<question_id>')
def display_question_and_answer(question_id):
    answers = mijenkcsihadjale.link_with_answer(question_id)


    return render_template('question_with_answer.html',answers = answers)


@app.route('/question/<question_id>/delete',methods = ['GET','POST'])
def delete_question(question_id):

    return redirect('/')


@app.route('/answer/<answer_id>/delete',methods = ['GET','POST'])
def delete_answer(answer_id):
    mijenkcsihadjale.del_answer(answer_id)
    return redirect('/')


@app.route("/question/<question_id>/vote-up", methods = ['POST','GET'])
def voteup(question_id):

    return redirect('/')


@app.route("/question/<question_id>/vote-down", methods = ['POST','GET'])
def votedown(question_id):

    return redirect('/')


@app.route("/answer/<answer_id>/vote-up", methods = ["GET", "POST"])
def answer_vote_up(answer_id):

    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/vote-down", methods = ['POST','GET'])
def answer_vote_down(answer_id):

    return redirect(f"/question/{question_id}")


@app.route('/answer/<question_id>/new-answer', methods=['POST', 'GET'])
def answer_questions(question_id):
    time = functions.current_time()

    if request.method == 'POST':

        return redirect(f"/answer/{question_id}")

    return render_template('new_answer.html', time=time)


@app.route('/added-answer/<question_id>', methods=['POST'])
def add_new_answer(question_id):

    if request.method == 'POST':

        return redirect('/')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
