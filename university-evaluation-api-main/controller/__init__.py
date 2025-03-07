# You can import controller here if you want to centralize the access
from .evaluation_controller import EvaluationController
from .home_controller import HomeController
from .degrees_controller import DegreesController
from .courses_controller import CoursesController
from .instructors_controller import InstructorsController
from .evaluation_controller import EvaluationController
from .departments_controller import DepartmentsController

def controller():
    """Return instances of all controller."""
    # Create and return instances of each controller
    # This function centralizes the creation of controller instances, making it easier to manage routes.
    return HomeController(), DegreesController(), CoursesController(), InstructorsController(), EvaluationController(), DepartmentsController()