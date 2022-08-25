from flask import Flask, render_template, redirect, url_for, request, flash, session

import bonus_questions
import functions
import mijenkcsihadjale
import os
from hash_password import hash_password, verify_password



app = Flask(__name__)
app.secret_key = "secret"

@app.route("/registration", methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('Username')
        email = request.form.get('email')
        password = hash_password(request.form.get('Password'))
        mijenkcsihadjale.register(username, password, email)
        return redirect(url_for('five_latest_questions'))
    else:
        return render_template('registration.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('username', None)
    session.pop('id', None)
    session.pop('loggedin', None)
    session.pop('reg_date', None)
    flash("You have been logged out", "info")
    return redirect(url_for('hello'))


@app.route("/")
def five_latest_questions():
    five_latest = mijenkcsihadjale.main_page_latest_five()
    if 'loggedin' in session:
        return render_template('main_page.html', questions=five_latest, logged=session['loggedin'])
    return render_template('main_page.html', questions=five_latest)


@app.route("/list")
def hello():
    order_by = request.args.get('ordering', 'id')
    questions = mijenkcsihadjale.main_page(order_by)
    if 'loggedin' in session:
        return render_template('main_page.html', questions=questions, logged=session['loggedin'])
    return render_template('main_page.html', questions=questions)




@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    add = True
    title = 'Add Question'
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            message = request.form.get('message')
            image = request.form.get('image')
            user_id = session['id']
            functions.add_question(title, message, image, user_id)
            # functions_data_manager, database_common
            return redirect('/')
    return render_template('add.html', add=add, title_name=title, logged=session['loggedin'])


@app.route('/update-question/<id_num>', methods=['GET', 'POST'])
def get_update_question(id_num):
    title_name = 'Update Question'
    question = functions.get_question(id_num)
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            message = request.form.get('message')
            image = request.form.get('image')
            functions.update_question(id_num, title, message, image)
            return redirect('/')
        return render_template('add.html', question=question, id_num=id_num,
                               add=False,
                               title_name=title_name, logged=session['loggedin'])


@app.route('/update-answer/<id_num>', methods=['GET', 'POST'])
def edit_answer(id_num):
    add = False
    title_name = 'update_answer'
    answer = functions.get_answer(id_num)
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            message = request.form.get('message')
            image = request.form.get('image')
            functions.update_answer(id_num, message, image)
            return redirect('/')
    return render_template('new_answer.html', answer=answer, answer_id=id_num,
                           add=False, title_name=title_name,
                           logged=session['loggedin']
    )


@app.route('/delete/<question_id>')
def delete_page(question_id):
    if 'loggedin' in session:
        img_src = mijenkcsihadjale.get_img_src(question_id)
        try:
            if img_src[0]['image']:
                os.remove(img_src[0]['image'])
        except FileNotFoundError:
            pass
        mijenkcsihadjale.del_question(question_id)
        return redirect('/')

@app.route('/add_accept/<answer_id>', methods=['GET', 'POST'])
def add_accept(answer_id):
    question_id = functions.accepting_answer(answer_id)['question_id']
    return redirect(url_for('display_question_and_answer', question_id=question_id))


@app.route('/question/<question_id>', methods=['GET'])
def display_question_and_answer(question_id):
    answers = mijenkcsihadjale.link_with_answer(question_id)
    comments = mijenkcsihadjale.display_comments(question_id)
    tag = mijenkcsihadjale.question_tag(question_id)
    user_for_this_question = functions.get_user_id_for_this_question(question_id)
    user_id = 0
    for row in user_for_this_question:
        user_id = row['user_id']
    if "loggedin" in session:
        if session["id"] == user_id:
            session["accept_value"] = True

            return render_template('question_with_answer.html', answers=answers, comments=comments,
                           tag=tag, accept_answer=session["accept_value"], logged=session['loggedin'])
    return render_template('question_with_answer.html', answers=answers, comments=comments,
                           tag=tag)

@app.route('/answer/<answer_id>/', methods=['GET', 'POST'])
def dislay_answer_comments(answer_id):
    comments = mijenkcsihadjale.display_comments_in_answer(answer_id)
    print(comments)
    return render_template('comment_for_answer.html', comments=comments)

@app.route('/comments/<comment_id>/delete')
def delete_comment_from_question(comment_id):
    mijenkcsihadjale.delete_comments_from_question(comment_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    mijenkcsihadjale.del_answer(answer_id)
    return redirect('/')


@app.route("/question/<question_id>/vote-up", methods=['POST', 'GET'])
def voteup(question_id):
    user_id = mijenkcsihadjale.get_user_id(question_id)['user_id']
    mijenkcsihadjale.vote_up(question_id,user_id)
    return redirect('/')


@app.route("/question/<question_id>/vote-down", methods=['POST', 'GET'])
def votedown(question_id):
    user_id = mijenkcsihadjale.get_user_id(question_id)['user_id']
    mijenkcsihadjale.vote_down(question_id, user_id)
    return redirect('/')


@app.route("/answer/<answer_id>/vote-down/<question_id>", methods=['POST', 'GET'])
def answer_vote_down(answer_id, question_id):
    user_id = mijenkcsihadjale.get_user_id_by_answer(answer_id)
    mijenkcsihadjale.answer_vote_down(answer_id,user_id)
    return redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/vote-up/<question_id>", methods=['POST', 'GET'])
def answer_vote_up(answer_id, question_id):
    user_id = mijenkcsihadjale.get_user_id_by_answer(answer_id)
    mijenkcsihadjale.answer_vote_up(answer_id,user_id)
    return redirect(f"/question/{question_id}")


@app.route('/search', methods=['POST'])
def search_question():
    expression = request.form.get('search')
    founded = functions.search_question(expression)
    return render_template('founded.html', questions=founded, expression=expression,
                           logged=session['loggedin'])



@app.route('/added-answer/<question_id>', methods=['GET', 'POST'])
def add_new_answer(question_id):
    add = True
    title = 'Add Answer'
    question = functions.get_question(question_id)
    if 'loggedin' in session:
        if request.method == 'POST':
            message = request.form.get('message')
            image = request.form.get('image')
            user_id = session['id']
            functions.add_answer(question_id, message, image, user_id)
            return redirect('/')
    return render_template('new_answer.html', question_id=question_id, add=add, title_name=title,
                           question=question, logged=session['loggedin'])



@app.route('/answer/<answer_id>/new-comment', methods= ['GET', 'POST'])
def add_answer_comment(answer_id):
    add = True
    if 'loggedin' in session:
        if request.method == 'GET':
            return render_template('add_comment.html',add=add, answer_id=answer_id, logged=session['loggedin'])
        elif request.method == 'POST':
            message = request.form.get('comment')
            user_id = session['id']

            question_id = mijenkcsihadjale.get_question_id(answer_id)
            mijenkcsihadjale.add_comment_to_answer(answer_id, message, user_id)
            return redirect(f"/question/{question_id[0]['question_id']}")

@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_question_comment(question_id):
    add = True
    if 'loggedin' in session:
        if request.method == 'GET':

            return render_template('add_comment_to_question.html', add=add, question_id=question_id, logged=session['loggedin'])

        elif request.method == 'POST':
            message = request.form.get('comment')
            user_id = session['id']
            mijenkcsihadjale.add_comment_to_question(question_id, message, user_id)
            return redirect("/")

@app.route('/edit/<id_num>/update-comment', methods=['GET', 'POST'])
def update_comment(id_num):
    add = False
    comment = functions.get_comment(id_num)
    if 'loggedin' in session:
        if request.method == 'POST':
            message = request.form.get('message')
            functions.update_comment(id_num, message)
            return redirect('/list')
        return render_template('add_comment.html', add=add, comment=comment, id_num=id_num, logged=session['loggedin'])


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag(question_id):
    if 'loggedin' in session:
        if request.method == 'GET':
            all_tag = mijenkcsihadjale.get_all_tag()
            return render_template('add_tag.html', question_id = question_id, all_tag=all_tag, logged=session['loggedin'])
        elif request.method == 'POST':
            tag = request.form.get('Tags')
            mijenkcsihadjale.add_tag(question_id, tag)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        account = functions.check_exist_user_by_username(username)
        if account:
            print(account)
            password_rs = account['user_password']
            if verify_password(password, password_rs):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['reg_date'] = account['registration_date']
                return redirect(url_for('hello'))
            else:
                flash('Incorrect: username / password')
        else:
            flash('Incorrect: username / password')
    return render_template('login.html')


@app.route('/all_users/', methods=['GET', 'POST'])
def get_all_users():
    users = functions.get_users()
    return render_template('users.html', users=users)

@app.route('/user/<user_id>', methods =['GET', 'POST'])
def user_page(user_id):
    user_question = mijenkcsihadjale.user_page_question(user_id)
    user_answer = mijenkcsihadjale.user_page_answer(user_id)
    user_comment = mijenkcsihadjale.user_page_comment(user_id)
    num_of_questions = len(user_question)
    num_of_ans  = len(user_answer)
    num_of_comments = len(user_comment)
    reputation = mijenkcsihadjale.get_reputation(session['id'])['reputation']
    return render_template('user_page.html', questions=user_question,
                               answers=user_answer, comments=user_comment,
                               asked_questions=num_of_questions,
                               number_of_answers=num_of_ans,
                               number_of_comments=num_of_comments,
                               reputation = reputation,
                                logged=session['loggedin'])

@app.route('/bonus-questions')
def bonus_question():
    return render_template('bonus_questions.html', questions = bonus_questions.SAMPLE_QUESTIONS)


@app.route('/tags')
def get_tags():
    tags = functions.get_tags()
    return render_template('tags.html', tags=tags)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
