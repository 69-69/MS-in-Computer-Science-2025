```aiignore
app/
│
├── app.py                    # Entry point of the application (Flask app setup)
│
├── model/                    # The Model directory (Handles the data logic)
│   ├── __init__.py           # Initialize model package
│   └── db_model.py           # Handles DB interaction and business logic
│
├── view/                     # The View directory (Responsible for rendering)
│   ├── __init__.py           # Initialize view package
│   ├── base_view.py          # Abstract view logic
│   ├── courses_view.py       # Renders courses-related data
│   ├── instructors_view.py   # Renders instructors-related data
│   ├── home_view.py          # Renders the home page
│   └── degrees_view.py       # Renders degrees-related data
│
├── controller/               # The Controller directory (Handles logic and data flow)
│   ├── __init__.py           # Initialize controller package
│   ├── home_controller.py    # Handles home page logic
│   ├── courses_controller.py # Fetches courses-related data
│   ├── instructors_controller.py # Fetches instructors-related data
│   └── degrees_controller.py # Fetches degrees-related data
│
├── static/                   # Static files and configuration
│   ├── __init__.py           # Initialize static package
│   ├── config.py             # Configuration settings (e.g., DB connection)
│   ├── create_tables.sql     # SQL script to create necessary tables
│   ├── error_handler.py      # Handles error logging and formatting
│   └── routes.py             # Defines routes and URL mappings
│  
├── config.properties         # Database config properties
│
└── README.md                 # Project documentation

```

# Key Components For Review (PR)

>**This configuration file defines settings for connecting to a database:**
<br> [database]
<br> host = localhost
<br> user = root
<br> password = root
<br> database = degree_evaluation

### 1. Model (model / )
- The Model handles the interaction with the database and encapsulates the application's business logic. The main file in this directory is db_model.py, which defines methods to interact with the MySQL database.

#### Files in Model:

> **__init__.py:** Initializes the model package.

> ** db_model.py:** Contains methods for data access and manipulation, including database connection handling, querying, and operations on tables.

```python
# Example (db_model.py):
    
class DBModel:
    def __init__(self):
        # Initialize DB connection and set up model
        pass

    def get_all_courses(self):
        # Query to get all courses from the database
        pass
```

### 2. View (view/)
- The View renders the user interface and displays data provided by the controller. In this project, views are typically responsible for rendering HTML templates or displaying data.

#### Files in View:

> **__init__.py:** Initializes the view package.

> **base_view.py:** This is a base class that can be extended by other views. It abstracts common rendering functionality.
<br> courses_view.py, <br> instructors_view.py, <br> home_view.py, <br> degrees_view.py: 
> <br><br> These files define specific views for their respective data types (Courses, Instructors, Home, Degrees).

```python
# Example (base_view.py):
    
class BaseView:
    def render(self, **kwargs):
        # This method will be used by all views to render the final page
        pass
```

### 3. Controller (controller / )
- The Controller acts as an intermediary between the Model and the View. It fetches data from the model, processes it (if necessary), and updates the view. Controllers handle user interactions and update views accordingly.

#### Files in Controller:

> **__init__.py:** Initializes the controller package.
<br> home_controller.py, <br> courses_controller.py, <br> instructors_controller.py, <br> degrees_controller.py: 
> <br><br> Each controller is responsible for a specific part of the application. It fetches data from the model and handles it appropriately before passing it to the view.

```python
# Example (home_controller.py):
    
from models.db_model import DBModel
from views.home_view import HomeView

class HomeController:
    def __init__(self):
        self.model = DBModel()
        self.view = HomeView()

    def index(self):
        courses = self.model.get_all_courses()
        return self.view.render(courses=courses)

```

### 4. Static (static/)
- The Static directory contains configuration files, error handling utilities, and routing logic.

#### Files in Static:

> **config.py:** Contains the database connection settings and other application configuration.

> **create_tables.sql:** SQL script to create tables in the MySQL database.

> **error_handler.py:** Provides centralized error handling for logging and formatting errors.

> **routes.py:** Defines the routes for the application and connects controllers to their corresponding routes.

```python
# Example: (routes.py):

from controllers.home_controller import HomeController
from controllers.courses_controller import CoursesController

class Routes:
    @staticmethod
    def init_routes(app):
        home_controller = HomeController()
        courses_controller = CoursesController()

        app.route('/')(home_controller.index)
        app.route('/courses')(courses_controller.index)
```


# CONFIGURATION:: Degree Evaluation Program

This project is an assignment of Group 11 for CS7330.

## Prerequisites

- Python 3.x
- MySQL server

## Setup

### 1. Clone the Repository

```bash
git clone git@github.com:aaron-martin/CS730_Group_11.git
cd degree-evaluation-program
```

### 2. Create and Configure the config.properties File
Create a config.properties file in the root directory of the project with the following content:

```
[database]
host = localhost
user = yourusername
password = yourpassword
database = degree_evaluation
Replace yourusername and yourpassword with your MySQL credentials.
```

### 3. Run the start.sh Script
The start.sh script will create a virtual environment, install the dependencies, and start the Flask server.

```
./start.sh
```
### 4. Access the Application
Once the server is running, you can access it in your web browser at http://127.0.0.1:8080/.