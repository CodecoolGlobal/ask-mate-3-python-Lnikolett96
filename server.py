from flask import Flask, render_template, redirect, url_for, request
import functions
import mijenkcsihadjale

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def hello(): # CSV file_open, ordering
    order_by = request.args.get('ordering')
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
def update_question(id_num):
    add = False
    update = True
    title_name = 'Update Question'
    time = functions.current_time()


    if request.method == 'POST':

        return redirect('/')
    return render_template('add.html', time=time,
                           submission_time=time, view_number=view_number,
                           vote_number=vote_number)

@app.route('/delete')
def delete_page():
    return render_template('delete_page.html')


@app.route('/question/<question_id>')
def display_question_and_answer(question_id): #answer_csv

    return render_template('question_with_answer.html',questions_again = answers)


@app.route('/question/<question_id>/delete',methods = ['GET','POST'])
def delete_question(question_id):

    return redirect('/')


@app.route('/answer/<answer_id>/delete',methods = ['GET','POST'])
def delete_answer(answer_id):

    return redirect(f'/question/{question_id}')


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
