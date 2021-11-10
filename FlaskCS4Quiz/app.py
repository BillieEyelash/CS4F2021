from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/output', methods=['POST'])
def output():
    email = request.form.get('email')
    return render_template('results.html', emailAddress=email)
