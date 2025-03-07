# view/home_view.py

from view.base_view import BaseView  # Import the BaseView class to inherit common rendering functionality


# View for the Home Route
class EvaluationView(BaseView):
    """View class for rendering the Evaluation page, inherits from BaseView."""

    def render(self, success, error, degrees, courses, goals, instructors, semesters, sections):
        """
        Renders the evaluation page with the given context (success, error, courses).
        This method is specific to rendering the home page and passes the necessary data to the template.

        :param success: A flag indicating whether the operation was successful
        :param error: An error message to be displayed if the operation failed
        :param courses: A list of courses to be displayed on the home page
        """

        # View-specific context for rendering the home page
        context = {
            'title': 'Evaluate Degree',  # Page title for the home page
            'subTitle': 'Degree Evaluation',  # Subtitle for the page
            'success': success,  # Success flag (whether the operation was successful)
            'error': error,
            'degrees': degrees,  
            'courses': courses,  # List of courses to display on the page
            'goals': goals,
            'instructors': instructors,
            'semesters': semesters,
            'sections': sections
        }

        # Call the render method from the BaseView class to render the 'index.html' template with the provided context
        return super().render('evaluation.html', **context)  # Use the parent class's render method to generate the HTML page

# class HomeView(BaseView):
#     def render(self, success, error, users):
# The specific implementation for rendering the home page
# return render_template('index.html', success=success, error=error, users=users)
