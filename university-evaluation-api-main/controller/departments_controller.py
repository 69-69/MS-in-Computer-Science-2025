from flask import request, redirect, url_for
from model import DBModel
from static.error_handler import ErrorHandler
from view.departments_view import DepartmentsView


# Controllers will handle the logic & send data to HTML Page

class DepartmentsController:
    def __init__(self):
        self.model = DBModel()
        self.view = DepartmentsView()

    def departments(self):
        if request.method == 'GET':
            try:
                # Fetch data for Add Goal and Evaluation features
                departments = self.model.get_all_departments()
                return self.view.render(
                    success=True,
                    error=None,
                    departments=departments
                )
            except Exception as e:
                return self.view.render(
                    success=False,
                    error=str(e),
                    departments = []
                )
        return redirect('/departments')

    def add_department(self):
        success = True
        error = ''

        try:
            if request.method == 'POST':
                # Retrieve form data
                name = request.form.get('name', '').strip()
                name = [name] # execute_query method requires an input in the form of a list, tuple, or dict

                if not name:
                    success = False
                    error = 'Please enter department name'
                else:
                    self.model.insert_department(name)

                    # Redirect to a confirmation or list page
                    return redirect("/departments")

        except Exception as e:
            success, error = ErrorHandler.handle_controller(e)

        return self.view.departments_form(success=success, error=error)






