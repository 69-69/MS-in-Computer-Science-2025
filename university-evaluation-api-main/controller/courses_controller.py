from model import DBModel
from view.courses_view import CoursesView
from flask import request, redirect, flash
from datetime import datetime

# The CoursesController class handles the logic for rendering the courses page.
# Controllers in the MVC pattern are responsible for the interaction between the model and the view.

class CoursesController:
    def __init__(self):
        # Initialize the controller with a view instance.
        self.model = DBModel()
        self.view = CoursesView()  # The view will handle the HTML rendering of course data
        self.course_sections = ['starting_value']
        self.semester_map = {
            'Spring': '-01-20',
            'Summer': '-07-01',
            'Fall': '-09-01'
        }

    def string_exists(self, value):
        return isinstance(value, str) and value

    def is_valid_date(self, date_string):
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def courses(self):
        # This method is responsible for rendering the courses page.
        # It delegates the rendering to the CoursesView.

        if request.method == 'GET':
            try:
                # Fetch data for Add Goal and Evaluation features
                courses = self.model.get_all_courses()
                instructors = self.model.get_all_instructors()
                semesters = self.model.get_all_semesters()
                sections = self.model.get_all_sections()
                return self.view.render(
                    success=True,
                    error=None,
                    courses=courses,
                    instructors=instructors,
                    semesters=semesters,
                    sections = sections,
                    course_sections = self.course_sections
                )
            except Exception as e:
                return self.view.render(
                    success=False,
                    error=str(e),
                    courses=[],
                    instructors=[],
                    semesters=[],
                    sections=[],
                    course_sections = []
                )
        return redirect('/courses')

    def add_course(self):
        """
        Handle the addition of a new course to the database.
        Redirects back to the evaluation page upon completion.
        """
        if request.method == 'POST':
            try:
                # Extract form data
                course_number = request.form['course_number']
                course_name = request.form['course_name']

                # Check validity of the entered course number
                # The last four characters should be digits. 
                # The other characters may be of variable lenghth and should be letters of the alphabet
                cn_length = len(course_number)
                last_four_idx = cn_length - 4
                last_four = course_number[last_four_idx:]
                prefix = course_number[0:last_four_idx]

                # Check if the last four characters of the entered course number are numeric
                last_four_valid = last_four.isdigit()
                # Check that all characters other than the last four are alphabetical
                prefix_valid = prefix.isalpha()

                if not (last_four_valid and prefix_valid):
                    flash('Invalid entry: Course number must start with a 2-4 letter departement code followed by a 4 digit number.', "error")
                    return redirect('/courses')

                # Insert the course into the database
                self.model.insert_course(course_number, course_name)

            except Exception as e:
                flash(f"Failed to add course: {str(e)}", "danger")
        return redirect('/courses')

    def add_section(self):
        """
        Handle the addition of a new course to the database.
        Redirects back to the evaluation page upon completion.
        """
        if request.method == 'POST':
            try:
                # Extract form data
                section_id = request.form['section_id']
                course_number = request.form['course_number']
                year = request.form['year']
                semester = request.form['semester']
                instructor_id = request.form['instructor_id']
                enrollment = request.form['enrollment']

                # Only accept positive section IDs
                if not (0 < int(section_id)):
                    flash('Invalid entry: The entered Section ID should be a positive number.', "error")
                    return redirect('/courses')

                # Only accept years that are given as a number
                if not (year.isdigit()):
                    flash('Invalid entry: The value for year must consist only of numbers.', "error")
                    return redirect('/courses')

                # Only accept years that are in our dropdown date range
                if not (2010 < int(year) < 2030):
                    flash('Invalid entry: The value for year must be between 2010 and 2030.', "error")
                    return redirect('/courses')

                # Only accept positive enrollment numbers
                if not (0 < int(enrollment)):
                    flash('Invalid entry: The entered Enrollment should be a positive number.', "error")
                    return redirect('/courses')

                # Insert the course into the database
                self.model.insert_section(section_id, course_number, year, semester, instructor_id, enrollment)

            except Exception as e:
                flash(f"Failed to add course: {str(e)}", "danger")
        return redirect('/courses')

    def get_course_sections(self):
        """
        Lists the sections of a course given a course number, a start year + semester and end year + semester
        Redirects back to the evaluation page upon completion.
        """
        if request.method == 'POST':
            try:
                course_number = request.form['course_number']
                beginning_year = request.form.get('beginning-year')
                beginning_semester = request.form.get('beginning-semester')
                ending_year = request.form.get('ending-year')
                ending_semester = request.form.get('ending-semester')

                all_values = [beginning_year, beginning_semester, ending_year, ending_semester]

                if any(not self.string_exists(element) for element in all_values):
                    flash('You must select beginning year, beginning semester, ending year, and ending semester', 'error')
                    return None

                beginning_year_semester = beginning_year + self.semester_map[beginning_semester]
                ending_year_semester = ending_year + self.semester_map[ending_semester]

                if not self.is_valid_date(beginning_year_semester) or not self.is_valid_date(beginning_year_semester):
                    return None, ['You must select a beginning year, beginning semester, ending year, and ending semester']
                if (datetime.strptime(ending_year_semester, '%Y-%m-%d') < datetime.strptime(beginning_year_semester, '%Y-%m-%d')):
                    flash('You must select a beginning year and semester that is not after the ending year and semester.')
                    return None

                # Query the course sections corresponding to the course number and time interval
                self.course_sections = self.model.get_course_sections(course_number, beginning_year_semester, ending_year_semester)

            except Exception as e:
                flash(f"Failed to add course: {str(e)}", "danger")

        return redirect('/courses')