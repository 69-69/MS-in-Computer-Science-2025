from flask import Flask
from static import init_app, init_database

app = Flask(__name__)
app.secret_key = 'CS7330-group-11-very-secret-key'
init_database(app) # Setup the database before any request

init_app(app) # Define the routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)