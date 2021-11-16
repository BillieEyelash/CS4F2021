from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.2122.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2122'
app.config['MYSQL_PASSWORD'] = 'm545CS42122'
app.config['MYSQL_DB'] = '2122project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

with open('recs.html') as f:
    lines = f.readlines()

recsDict = {}
currentGenre = ''
currentRecs = []
for line in lines:
    if ',' not in line:
        if currentGenre != '':
            recsDict[currentGenre] = currentRecs
        currentGenre = line
    else:
        book, author = line.split(", ")
        currentRecs.append((book, author))

cur = mysql.connection.cursor()
for genre, recs in recsDict:
    q = "INSERT INTO `riatalwar_genres`(`genre`) VALUES (%s)"
    qVars = (genre,)
    id = execute_query(cur, q, qVars)
    q = "SELECT id FROM `riatalwar_genres` WHERE genre = %s"
    qVars = (genre,)
    id = execute_query(cur, q, qVars)
    q = "INSERT INTO `riatalwar_recommendatons`(`title`, `author`, `genre_id`) VALUES (%s, %s, %s)"
    for r in recs:
        qVars = (r[0], r[1], id)
        execute_query(cur, q, qVars)


def execute_query(cursor, query, queryVars=()):
    ''' Description: Execute the given query
        Parameters: Cursor, String query, Tuple optional query variables
        Return: Query results '''
    # Check if there are variables to plug in
    if len(queryVars) == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, queryVars)
    cursor.connection.commit()
    return cursor.fetchall()
