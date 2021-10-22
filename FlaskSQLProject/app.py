from flask import Flask, render_template, request

app = Flask(__name__)

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
    inputName = request.form.get("firstname"), request.form.get("lastname")
    passwords = request.form.get("password"), request.form.get("passconfirm")
    passwordInput = passwords[0]
    emailInput = request.form.get("email")
    # Stay at form if input is invalid
    if not valid_input(inputName, passwords, emailInput):
        return index()

    genreInput = request.form.getlist("genre")
    booksReadInput = request.form.get("booksread")
    return render_template('results.html', name=inputName, password=passwords[0], email=emailInput, genres=genreInput, booksRead=booksReadInput)


def valid_input(name, passwords, email):
    ''' Description: Determine whether or not the given inputs are valid
        Parameters: List [first, last name], List [password, confirm password], String email
        Return: Boolean name, password, and email are valid '''
    # Check if name is blank
    if name[0] == "" or name[1] == "":
        return False
    # Check if passwords don't match or are blank
    elif passwords[0] != passwords[1] or passwords[0] == "":
        return False
    # Check if is valid email
    elif "@" not in email:
        return False
    return True
