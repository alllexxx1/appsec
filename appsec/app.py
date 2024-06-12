import os
import json

from flask import (
    Flask, redirect, url_for, request,
    session, render_template, jsonify
)

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the flask app with the secret key
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route(rule='/')
def index():
    """
    Root route of the application.
    If the user is logged in, render the index.html template.
    Otherwise, redirect to the login page.
    """
    if session.get('logged_in'):
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route(rule='/login', methods=['GET', 'POST'])
def login():
    """
    Handle login functionality.
    - For GET requests, render the login.html template if not logged in, else render index.html.
    - For POST requests, process login form submission and redirect based on credentials.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('login_success'))
        else:
            return redirect(url_for('login_fail'))

    elif request.method == 'GET':
        if session.get('logged_in'):
            return render_template('index.html')
        return render_template('login.html')


@app.route(rule='/login_success')
def login_success():
    """
    Transition to appsec practices in a case of successful login.
    If the user is logged in, render the login_success.html template
    with flash message about successful login.
    Otherwise, redirect to the login page.
    """
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('login_success.html')


@app.route(rule='/login_fail')
def login_fail():
    """
    Handler rendering login_fail.html with a friendly message
    about necessity to insert valid credentials.
    """
    return render_template('login_fail.html')


@app.route(rule='/logout')
def logout():
    """
    Log out the user by setting session 'logged_in' to False.
    Redirect to the login page.
    """
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route(rule='/appsec')
def appsec():
    """
    Route to provide information about security practices.
    If the user is logged in, retrieve the information from the appsec.json file based on the key parameter.
    Return the information as JSON.
    If the user is not logged in, redirect to the login page.

    Parameters:
    - key: The key to look up in the appsec.json file (query parameter).
    """
    if session.get('logged_in'):

        key = request.args.get('key')
        with open('appsec/appsec.json') as f:
            data = json.load(f)
        practice_info = data.get(key, 'Invalid key')

        return jsonify({key: practice_info})

    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors (page not found).
    Render the errors/404.html template.
    """
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """
    Handle 500 errors (server error).
    Render the errors/500.html template.
    """
    return render_template('errors/500.html'), 500
