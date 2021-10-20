from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.2122.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2122'
app.config['MYSQL_PASSWORD'] = 'm545CS42122'
app.config['MYSQL_DB'] = '2122playground'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM riatalwar_test'
    cursor.execute(query)
    mysql.connection.commit()
    data = cursor.fetchall()
   return render_template('index.html', rows=data)
