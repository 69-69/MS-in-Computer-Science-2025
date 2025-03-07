# view/courses_view.py

from view.base_view import BaseView  # Import the BaseView class to inherit common rendering functionality


# View for the Courses Route
class CoursesView(BaseView):
    """View class for rendering the Courses page, inherits from BaseView."""

    def render(self, success, error, courses, instructors, semesters, sections, course_sections):
        """
        The specific implementation for rendering the courses page.
        This method defines the context (data) to be passed to the template.
        """
        # Context data for rendering the courses page
        context = {
            'title': 'Welcome to the Courses Page',  # Page title
            'subTitle': 'Add Course Information',  # Subtitle for the page
            'success': success,  # Success flag (whether the operation was successful)
            'error': error,
            'courses': courses,  # List of courses to display on the page
            'instructors': instructors,
            'semesters': semesters,
            'sections': sections,
            'course_sections': course_sections
        }

        # Call the render method from the BaseView class to render the 'courses.html' template with the context
        return super().render('courses.html',
                              **context)  # Use the parent class's render method to generate the final HTML
