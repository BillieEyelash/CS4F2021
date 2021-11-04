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
    ''' Description: Launch the home page which contains the form
        Parameters: None
        Return: Form page '''
    genreList = ["Nonfiction", "Realistic Fiction", "Fantasy", "Science Fiction", "Adventure",
            "Classics", "Mystery", "Horror", "Graphic Novel", "Historical Fiction", "Romance"]
    genreList.sort()
    return render_template('index.html', genres=genreList)


@app.route('/results', methods=['POST'])
def results():
    ''' Description: Launch the results page and retrieve input from form
        Parameters: None
        Return: Webpage for form or results '''
    # Retrieve form input
    nameInput = request.form.get("firstname") + " " + request.form.get("lastname")
    usernameInput = request.form.get("username")
    passwords = request.form.get("password"), request.form.get("passconfirm")
    passwordInput = passwords[0]
    emailInput = request.form.get("email")
    # Stay at form if input is invalid
    if not valid_input(nameInput, usernameInput, passwords, emailInput):
        return index()
    # Get remaining inputs
    genreInput = request.form.getlist("genre")
    booksReadInput = int(request.form.get("booksread"))

    cursor = mysql.connection.cursor()

    # Insert data into table
    query = "INSERT INTO `riatalwar_form` (`name`, `username`, `password`, `email`, `books_read`) VALUES (%s, %s, %s, %s, %s);"
    queryVars = (nameInput, usernameInput, passwordInput, emailInput, booksReadInput)
    execute_query(query, queryVars, cursor)

    # Usernames have to be unique
    query = "SELECT id FROM `riatalwar_form` WHERE username=%s;"
    queryVars = (usernameInput,)
    id = execute_query(query, queryVars, cursor)[0]['id']

    for genre in genreInput:
        # Get genre id if already in genre table
        query = "SELECT id FROM `riatalwar_genres` WHERE genre=%s"
        queryVars = (genre,)
        idData = execute_query(query, queryVars, cursor)
        # Add genre to table if necessary
        if len(idData) == 0:
            query = "INSERT INTO `riatalwar_genres` (`genre`) VALUES (%s)"
            execute_query(query, queryVars, cursor)
            # Get genre id
            query = "SELECT id FROM `riatalwar_genres` WHERE genre=%s"
            idData = execute_query(query, queryVars, cursor)
        genreID = idData[0]['id']
        # Add favorite genre to table
        query = "INSERT INTO `riatalwar_favorite_genres` (`person_id`, `genre_id`) VALUES (%s, %s)"
        queryVars = (id, genreID)
        execute_query(query, queryVars, cursor)

    query = "SELECT username FROM riatalwar_form WHERE NOT id=%s AND id IN (SELECT person_id FROM riatalwar_favorite_genres WHERE genre_id IN (SELECT genre_id FROM riatalwar_favorite_genres WHERE genre_id IN (SELECT genre_id FROM riatalwar_favorite_genres WHERE person_id=%s)))"
    queryVars = (id, id)
    personData = execute_query(query, queryVars, cursor)
    people = set()
    for p in personData:
        people.add(p['username'])
    return render_template('results.html', p=people)


def valid_input(name, username, passwords, email):
    ''' Description: Determine whether or not the given inputs are valid
        Parameters: List [first, last name], List [password, confirm password], String email
        Return: Boolean name, password, and email are valid '''
    # Check if name is blank
    if name[0] == "" or name[1] == "":
        return False

    cursor = mysql.connection.cursor()
    query = "SELECT * FROM riatalwar_form WHERE username=%s"
    queryVars = (username,)
    if len(execute_query(query, queryVars, cursor)) != 0:
        return False

    # Check if passwords don't match or are blank
    elif passwords[0] != passwords[1] or passwords[0] == "":
        return False
    # Check if is valid email
    elif "@" not in email:
        return False
    return True


def execute_query(query, queryVars, cursor):
    ''' Description: Execute the given query
        Parameters: String query, Tuple query variables, Cursor
        Return: Query results '''
    cursor.execute(query, queryVars,)
    cursor.connection.commit()
    return cursor.fetchall()
