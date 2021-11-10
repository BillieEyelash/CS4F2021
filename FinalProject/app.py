from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.2122.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2122'
app.config['MYSQL_PASSWORD'] = 'm545CS42122'
app.config['MYSQL_DB'] = '2122project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    ''' Description: Launch the home page which contains the form
        Parameters: None
        Return: Home page '''
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    ''' Description: Launch the results page and retrieve input from form
        Parameters: None
        Return: Search results page '''
    # get search results from API
    return render_template('search.html')


@app.route('/recommendations')
def recommendations():
    ''' Description: Launch the recommendations page and get recommendations from database
        Parameters: None
        Return: Recommendations page '''
    cur = mysql.connection.cursor()
    # Get all genres stored in database
    q = "SELECT id, genre FROM `riatalwar_genres`"
    genres = execute_query(cur, q)

    r = {}  # Create dictionary to store recs for each genre
    for pair in genres:
        id = pair['id']
        # Get all recs for a certain genre
        q = "SELECT author, title FROM `riatalwar_recommendatons` WHERE genre_id=%s"
        qVars = (id,)
        recsDict = execute_query(cur, q, qVars)
        
        # Make an alphabetical list of recommendations
        recsList = [(rec['title'] + " by " + rec['author']) for rec in recsDict]
        recsList.sort()
        # Store recs for genre in dict
        r[pair['genre']] = recsList

    return render_template('recommendations.html', recs=r)


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
