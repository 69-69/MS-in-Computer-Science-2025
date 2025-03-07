# view/instructors_view.py

from view.base_view import BaseView


# View class for rendering the Instructors page, inherits from BaseView.
class InstructorsView(BaseView):

    def render(self, success, error, instructors):
        context = {
            'title': 'Welcome to the Instructors Page',
            'subTitle': 'List Instructors',
            'success': success,
            'error': error,
            'instructors': instructors,
        }

        # Call the render method from the BaseView (Parent) class to render the 'index.html' template with the provided context (Data)
        return super().render('instructors.html', **context)

    def instructor_form(self, success, error):
        context = {
            'title': 'Add Instructor',
            'subTitle': "Add New Instructor",
            'success': success,
            'error': error,
        }

        # Call the render method from the BaseView (Parent) class to render the 'index.html' template with the provided context (Data)
        return super().render('instructor_form.html', **context)

    def render_instructor_query(self, **context):
        return super().render('instructor_query_form.html', **context)
