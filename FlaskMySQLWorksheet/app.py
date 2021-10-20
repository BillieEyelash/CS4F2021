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
    # Set up MySQL object which can be used for multiple queries
    cursor = mysql.connection.cursor()
    # Define query string
    query = 'SELECT * FROM riatalwar_test'
    # Execute (actually run) the predefined query
    cursor.execute(query)
    # Commit query (necessary when executing multiple queries)
    mysql.connection.commit()
    # Fetches all rows returned by the query (only necessary when getting information)
    # The data is returned as a multidimensional associative array
    data = cursor.fetchall()
    return render_template('index.html', rows=data)
