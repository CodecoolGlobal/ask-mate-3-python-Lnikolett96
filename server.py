from flask import Flask, render_template, redirect, url_for, request
import functions
import mijenkcsihadjale
import os

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def hello():
    order_by = request.args.get('ordering', 'id')
    questions = mijenkcsihadjale.main_page(order_by)
    return render_template('main_page.html', questions=questions)


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

    img_src = mijenkcsihadjale.get_img_src(question_id)
    try:
        if img_src[0]['image']:
            os.remove(img_src[0]['image'])
    except FileNotFoundError:
        pass
    mijenkcsihadjale.del_question(question_id)
    return redirect('/')




@app.route('/question/<question_id>')
def display_question_and_answer(question_id):

    answers = mijenkcsihadjale.link_with_answer(question_id)
    comments = mijenkcsihadjale.display_comments(question_id)
    print(comments)
    return render_template('question_with_answer.html', answers=answers, comments=comments)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    mijenkcsihadjale.del_answer(answer_id)
    return redirect('/')


@app.route("/question/<question_id>/vote-up", methods=['POST', 'GET'])
def voteup(question_id):
    mijenkcsihadjale.vote_up(question_id)
    return redirect('/')


@app.route("/question/<question_id>/vote-down", methods=['POST', 'GET'])
def votedown(question_id):
    mijenkcsihadjale.vote_down(question_id)
    return redirect('/')


@app.route("/answer/<answer_id>/vote-down/<question_id>", methods=['POST', 'GET'])
def answer_vote_down(answer_id, question_id):
    mijenkcsihadjale.answer_vote_down(answer_id)

    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/vote-up/<question_id>", methods=['POST', 'GET'])
def answer_vote_up(answer_id, question_id):
    mijenkcsihadjale.answer_vote_up(answer_id)
    return redirect(f"/question/{question_id}")

@app.route('/')
@app.route('/search', methods=['POST'])
def search_question():
    expression = request.form.get('search')
    founded = functions.search_question(expression)
    return render_template('founded.html', questions=founded, expression=expression)


@app.route('/added-answer/<question_id>', methods=['GET', 'POST'])
def add_new_answer(question_id):
    add = True
    title = 'Add Answer'
    question = functions.get_question(question_id)
    if request.method == 'POST':
        message = request.form.get('message')
        image = request.form.get('image')
        functions.add_answer(question_id, message, image)
        return redirect('/')
    return render_template('new_answer.html', question_id=question_id, add=add, title_name=title, question=question)


@app.route('/answer/<answer_id>/new-comment', methods= ['GET', 'POST'])
def add_answer_comment(answer_id):
    if request.method == 'GET':
        return render_template('add_comment.html', answer_id=answer_id)
    elif request.method == 'POST':
        message = request.form.get('comment')
        question_id = mijenkcsihadjale.get_question_id(answer_id)
        mijenkcsihadjale.add_comment_to_answer(answer_id, message)
        return redirect(f"/question/{question_id[0]['question_id']}")

@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_question_comment(question_id):
    if request.method == 'GET':

        return render_template('add_comment_to_question.html', question_id=question_id)

    elif request.method == 'POST':
        message = request.form.get('comment')
        print(question_id)
        mijenkcsihadjale.add_comment_to_question(question_id, message)
        return redirect("/")


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
