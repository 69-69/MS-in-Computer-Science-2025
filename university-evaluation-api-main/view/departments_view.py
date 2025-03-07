# view/departments_view.py

from view.base_view import BaseView


# View class for rendering the Departments page, inherits from BaseView.
class DepartmentsView(BaseView):

    def render(self, success, error, departments):
        context = {
            'title': 'Welcome to the departments Page',
            'subTitle': 'List Departments',
            'success': success,
            'error': error,
            'departments': departments
        }

        # Call the render method from the BaseView (Parent) class to render the 'index.html' template with the provided context (Data)
        return super().render('departments_form.html', **context)

    def departments_form(self, success, error):
        context = {
            'title': 'Add Departments',
            'subTitle': "Add New Departments",
            'success': success,
            'error': error
        }

        # Call the render method from the BaseView (Parent) class to render the 'index.html' template with the provided context (Data)
        return super().render('departments_form.html', **context)
