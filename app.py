from ngram_models import Ngram
from flask import Flask, render_template

with open("data_files/nietzsche.txt", "r", encoding="utf-8") as f:
    textComplete = f.read()
textComplete = textComplete[15025:-1054]
model = Ngram(textComplete, 3)
app = Flask(__name__)

@app.route("/")
def index():
    #return "hello world"
    return render_template("Nietzsche.html", quote="")


@app.route("/nietzsche")
def nietzsche():
    return render_template("Nietzsche.html", quote=model.generate(5))

if __name__ == '__main__':
   app.run()    