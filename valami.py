from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def alap():
    return 'Ez lesz az oldal.'


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    add = True
    title = 'Add Question'
    if request.method == 'POST':
        return redirect(url_for('main_page.html'))
    return render_template('add.html', add=add, title=title)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
