from flask import Flask, render_template
from math import factorial

app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('index.html', myVar=7, myList=['a', 'b', 'c'])

@app.route('/factorial')
def factorialPage():
    factorials = []
    for i in range(10):
        factorials.append(calculateFactorial(i + 1))
    return render_template('factorial.html', f=factorials)
def calculateFactorial(n):
    return factorial(n)
