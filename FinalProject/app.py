from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from os import listdir

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
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' Description: Launch signup page and add users
        Parameters: None
        Return: Signup page '''
    if request.method == 'GET':
        return render_template('signup.html', error=request.args.get('error'))

    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    cur = mysql.connection.cursor()
    # If username already in database --> error
    q = 'SELECT * FROM riatalwar_users WHERE username = %s'
    qVars = (username,)
    if len(execute_query(cur, q, qVars)) > 0:
        return redirect(url_for('signup', error=True))
    # If username is too long/short --> error
    elif len(username) > 50 or len(username) == 0:
        return redirect(url_for('signup', error=True))
    # If password is too short --> error
    elif len(password) == 0:
        return redirect(url_for('signup', error=True))
    # If passwords don't match --> error
    elif password != confirm:
        return redirect(url_for('signup', error=True))

    # Insert username/password into database --> login
    securedPass = generate_password_hash(password)
    q = 'INSERT INTO riatalwar_users(username, password) VALUES (%s, %s)'
    qVars = (username, securedPass)
    execute_query(cur, q, qVars)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Description: Launch login page and log in users
        Parameters: None
        Return: Login page '''
    if request.method == 'GET':
        return render_template('login.html', error=request.args.get('error'))
    username = request.form.get('username')
    password = request.form.get('password')
    # Search database for username/password
    cur = mysql.connection.cursor()
    q = 'SELECT password FROM riatalwar_users WHERE username = %s'
    qVars = (username,)
    results = execute_query(cur, q, qVars)

    # Invalid username --> error
    if len(results) == 0:
        return redirect(url_for('login', error=True))
    # Correct username and password --> home
    elif check_password_hash(results[0]['password'], password):
        session['riatalwar_username'] = username
        return redirect(url_for('index'))
    # Invalid password --> error
    else:
        return redirect(url_for('login', error=True))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    ''' Description: Logout user and redirect to home page
        Parameters: None
        Return: Home page '''
    session.pop('riatalwar_username', None)
    return redirect(url_for('index'))


@app.route('/changepass', methods=['GET', 'POST'])
def changepass():
    ''' Description: Change password
        Parameters: None
        Return: Profile page '''
    oldpass = request.form.get('oldpass')
    newpass = request.form.get('newpass')
    confirm = request.form.get('confirm')
    # Search database for username/password
    username = session.get('riatalwar_username', None)
    cur = mysql.connection.cursor()
    q = 'SELECT password FROM riatalwar_users WHERE username = %s'
    qVars = (username,)
    password = execute_query(cur, q, qVars)[0]['password']

    # If old passwords don't match
    if not check_password_hash(password, oldpass):
        return redirect(url_for('profile', error='Incorrect password.'))
    # If new passwords don't match
    elif newpass != confirm:
        return redirect(url_for('profile', error='Passwords do not match.'))
    # If password length == 0
    elif len(newpass) == 0:
        return redirect(url_for('profile', error='Invalid password.'))

    # Update database if no errors
    q = 'UPDATE riatalwar_users SET password = %s WHERE username = %s'
    qVars = (generate_password_hash(newpass), username)
    execute_query(cur, q, qVars)
    return redirect(url_for('profile'))


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    ''' Description: Delete account and redirect to home page
        Parameters: None
        Return: Home page '''
    username = session.pop('riatalwar_username', None)
    cur = mysql.connection.cursor()
    q = 'DELETE FROM riatalwar_users WHERE username = %s'
    qVars = (username,)
    execute_query(cur, q, qVars)
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    ''' Description: Get API data and display results
        Parameters: None
        Return: Search results page '''
    # get search results from API
    q = request.form.get('query')
    req = 'https://www.googleapis.com/books/v1/volumes?q=intitle:' + q + '&printType=books&orderBy=relevance'
    response = requests.get(req)
    jsonResp = response.json()
    # No results so skip loop
    if jsonResp['totalItems'] == 0:
        return render_template('search.html', books=None)

    books = []
    items = jsonResp['items']
    for i in range(len(items)):
        volInfo = items[i]['volumeInfo']
        book = {}
        book['title'] = volInfo['title']
        # Try to get all information but it is not always there
        try:
            book['author'] = volInfo['authors'][0]
        except:
            book['author'] = None
        try:
            book['description'] = volInfo['description']
        except:
            book['description'] = None
        try:
            book['img'] = volInfo['imageLinks']['thumbnail']
        except:
            book['img'] = None
        # Create unique id
        book['id'] = book['title'].replace(' ', '--') + '++' + book['author'].replace(' ', '--') + str(i)
        book['id'] = book['id'].replace('.', '')

        # Check if there is a review and store filename
        book['review'] = None
        dir = listdir('public/RiaTalwar/FinalProject/reviews')
        if book['id'][:-len(str(i))] + '.txt' in dir:
            book['review'] = book['id'][:-len(str(i))] + '.txt'
        books.append(book)
    return render_template('search.html', books=books)


@app.route('/review', methods=['GET'])
def review():
    ''' Description: Display review
        Parameters: None
        Return: Review page '''
    file = request.args.get('file')
    # Get review
    f = open('public/RiaTalwar/FinalProject/reviews/' + file)
    lines = [line.strip() for line in f.readlines()]
    lines[0] = lines[0].strip('ï»¿')
    # Get title and author
    t, a = file.replace('--', ' ').strip('.txt').split('++')
    return render_template('review.html', review=lines, title=t, author=a)


@app.route('/addBook', methods=['POST'])
def addBook():
    ''' Description: Add a book to user's books
        Parameters: None
        Return: success/error '''
    # Get title and author
    book = request.form.get('book')
    title, author = book.split()
    title = title.replace('--', ' ')
    author = author.replace('--', ' ')
    while author[-1].isnumeric():
        author = author[:-1]

    cur = mysql.connection.cursor()
    # Get current user id
    q = 'SELECT id FROM riatalwar_users WHERE username = %s'
    qVars = (session.get('riatalwar_username'),)
    if qVars[0] == None:
        return 'error'
    id = execute_query(cur, q, qVars)[0]['id']

    # Check if book was already saved by user
    q = 'SELECT id FROM riatalwar_user_books WHERE title = %s AND author = %s AND user_id = %s'
    qVars = (title, author, id)
    books = execute_query(cur, q, qVars)
    # If not saved, add book
    if len(books) == 0:
        q = 'INSERT INTO riatalwar_user_books (title, author, user_id) VALUES (%s, %s, %s)'
        qVars = (title, author, id)
        execute_query(cur, q, qVars)
    return 'success'


@app.route('/removeBook', methods=['POST'])
def removeBook():
    ''' Description: Remove book from user's account
        Parameters: None
        Return: success '''
    # Get title and author
    book = request.form.get('book')
    title, author = book.split()
    title = title.replace('--', ' ')
    author = author.replace('--', ' ')

    cur = mysql.connection.cursor()
    # Get current user id
    q = 'SELECT id FROM riatalwar_users WHERE username = %s'
    qVars = (session.get('riatalwar_username'),)
    id = execute_query(cur, q, qVars)[0]['id']
    # Remove book from database
    q = 'DELETE FROM riatalwar_user_books WHERE title = %s AND author = %s AND user_id = %s'
    qVars = (title, author, id)
    execute_query(cur, q, qVars)
    return 'success'


@app.route('/recommendations')
def recommendations():
    ''' Description: Get and display recommendations from database
        Parameters: None
        Return: Recommendations page '''
    cur = mysql.connection.cursor()
    # Get all genres stored in database
    q = 'SELECT id, genre FROM riatalwar_genres'
    genres = execute_query(cur, q)

    recs = []  # Create dictionary to store recs for each genre
    i = 0
    for pair in genres:
        id = pair['id']
        # Get all recs for a certain genre
        q = 'SELECT author, title FROM riatalwar_recommendatons WHERE genre_id=%s'
        qVars = (id,)
        recsDict = execute_query(cur, q, qVars)

        # Make a list of recommendations
        recsList = []
        for rec in recsDict:
            display = rec['title'] + ' by ' + rec['author']
            # Create unique id
            id = rec['title'].replace(' ', '--') + '++' + rec['author'].replace(' ', '--') + str(i)
            recsList.append((display, id))
            i += 1
        recs.append((pair['genre'], recsList))
    return render_template('recommendations.html', items=recs)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    ''' Description: Launch the profile page
        Parameters: None
        Return: Profile page '''
    if session.get('riatalwar_username') == None:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session.get('riatalwar_username'), error=request.args.get('error'))


@app.route('/yourbooks')
def yourbooks():
    ''' Description: Launch the yourbooks page to display user's books
        Parameters: None
        Return: Yourbooks page '''
    username = session.get('riatalwar_username')
    if username == None:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    # Get user id so you can find their books
    q = 'SELECT id FROM riatalwar_users WHERE username = %s'
    qVars = (session['riatalwar_username'],)
    id = execute_query(cur, q, qVars)[0]['id']
    # Get books
    q = 'SELECT title, author FROM riatalwar_user_books WHERE user_id = %s'
    qVars = (id,)
    results = execute_query(cur, q, qVars)
    books = []
    for result in results:
        id = result['title'].replace(' ', '--') + '++' + result['author'].replace(' ', '--')
        books.append((result['title'], result['author'], id))
    return render_template('yourbooks.html', books=books)


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
