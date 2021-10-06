from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    inputtedName = request.form.get("fullname")
    sushiInput = request.form.get("sushi")
    vehicleInput = request.form.getlist("vehicle")
    return render_template('results.html', name=inputtedName, sushi=sushiInput, vehicles=vehicleInput)
