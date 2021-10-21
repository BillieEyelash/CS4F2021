from flask import Flask, render_template, request
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
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    name = request.form.get("searchname")
    # Set up MySQL object which can be used for multiple queries
    cursor = mysql.connection.cursor()
    # Define query string
    query = "SELECT * FROM riatalwar_test WHERE name=%s;"
    # List of variables to insert into query
    queryVars = (name,)
    # Execute (actually run) the predefined query
    cursor.execute(query, queryVars)
    # Commit query (necessary when executing multiple queries)
    mysql.connection.commit()
    # Fetches all rows returned by the query (only necessary when getting information)
    # The data is returned as a multidimensional associative array
    data = cursor.fetchall()
    return render_template("results.html", numPeople=len(data))
