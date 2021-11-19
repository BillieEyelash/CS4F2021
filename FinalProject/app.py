from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.2122.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2122'
app.config['MYSQL_PASSWORD'] = 'm545CS42122'
app.config['MYSQL_DB'] = '2122project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'kjstghweujkdssioe'
mysql = MySQL(app)

@app.route('/')
def index():
    ''' Description: Launch the home page
        Parameters: None
        Return: Home page '''
    return render_template('index.html', username=session.get('riatalwar_username'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' Description: Launch the login page
        Parameters: None
        Return: Signup page '''
    if request.method == 'GET':
        return render_template('signup.html')
    username = request.form.get('username')
    if len(username) > 50:
        return redirect(url_for('signup', error=True))
    password = request.form.get('password')
    securedPass = generate_password_hash(password)
    cur = mysql.connection.cursor()
    q = 'INSERT INTO riatalwar_users(username, password) VALUES (%s, %s)'
    qVars = (username, securedPass)
    execute_query(cur, q, qVars)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Description: Launch the login page
        Parameters: None
        Return: Login page '''
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    q = 'SELECT password FROM riatalwar_users WHERE username=%s'
    qVars = (username,)
    results = execute_query(cur, q, qVars)
    if len(results) == 0: # Invalid username
        return redirect(url_for('login', error=True))
    elif check_password_hash(results[0]['password'], password): # Correct username and password
        session['riatalwar_username'] = username
        return redirect(url_for('index'))
    else: # Incorrect password
        return redirect(url_for('login', error=True))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    ''' Description: Logout user and redirect to home page
        Parameters: None
        Return: Home page '''
    session.pop('riatalwar_username', None)
    return redirect(url_for('index'))


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


@app.route('/profile')
def profile():
    ''' Description: Launch the profile page
        Parameters: None
        Return: Profile page '''
    if session.get('riatalwar_username') == None:
        return redirect(url_for('signup'))
    return render_template('profile.html')


@app.route('/yourbooks')
def yourbooks():
    ''' Description: Launch the yourbooks page to display user's books
        Parameters: None
        Return: Yourbooks page '''
    return render_template('yourbooks.html')


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
