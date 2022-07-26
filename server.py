from flask import Flask, render_template
import csv

app = Flask(__name__)


@app.route("/")
def hello():
    questions = []
    with open("./sample_data/question.csv", "r") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        for row in spamreader:
            print(row)
            questions.append(row)


    return render_template('main_page.html', questions = questions)




if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
