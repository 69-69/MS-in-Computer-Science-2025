from model.db_model import DBModel
from view.home_view import HomeView
from flask import request
from static.error_handler import ErrorHandler


# Controllers will handle the logic & send data to HTML Page

class HomeController:
    def __init__(self):
        self.model = DBModel()
        self.view = HomeView()

    def index(self):

        success = True
        error = ''
        evaluations = None

        try:
            if request.method == 'POST' and request.form.get('reset-action') == 'reset-database':
                self.model.reset_database()

            evaluations = self.model.get_all_evaluations()

            if not evaluations:
                error = "No evaluations found."

        except Exception as e:
            print('error in controller', e)
            success, error = ErrorHandler.handle_controller(e)

        return self.view.render(success=success, error=error, evaluations=evaluations)
