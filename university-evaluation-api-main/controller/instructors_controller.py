from flask import request, redirect, url_for
from model import DBModel
from static.error_handler import ErrorHandler
from view.instructors_view import InstructorsView


# Controllers will handle the logic & send data to HTML Page

class InstructorsController:
    def __init__(self):
        self.model = DBModel()
        self.view = InstructorsView()

    def add_instructor(self):
        success = True
        error = ''

        try:
            if request.method == 'POST':
                # Retrieve form data
                name = request.form.get('name', '').strip()

                if not name:
                    success = False
                    error = 'Please enter instructor ID and name'
                else:
                    self.model.insert_instructor(name)

                    # Redirect to a confirmation or list page
                    return redirect(url_for('instructors'))

        except Exception as e:
            success, error = ErrorHandler.handle_controller(e)

        return self.view.instructor_form(success=success, error=error)

    def instructors(self):
        """Render the instructors page."""
        success = True
        error = ''
        instructors = None

        try:
            instructors = self.model.get_all_instructors()

            if not instructors:
                error = 'No instructors found'

        except Exception as e:
            success, error = ErrorHandler.handle_controller(e)

        return self.view.render(success=success, error=error, instructors=instructors)

    def instructor_query(self):

        instructors = self.model.get_all_instructors()
        years = self.model.get_all_years()
        context = {
            'instructors': instructors,
            'years': years
        }

        try:
            if request.method == 'POST':
                # Retrieve form data
                instructor_id = request.form['instructor_id']
                start_year = int(request.form['start_year'])
                end_year = int(request.form['end_year'])

                if instructor_id == None or start_year == None or end_year == None:
                    success = False
                    error = 'All fields are required'
                    context.update({'success': success, 'error': error})
                else:
                    # Query the sections taught by the instructor
                    sections = self.model.get_sections_by_instructor(instructor_id, start_year, end_year)
                    # Filter the list of instructors to find the instructor with the provided ID
                    filtered_instructor = next(
                        (instructor for instructor in instructors if instructor['instructor_id'] == instructor_id),
                        None
                    )

                    # If instructor is found, retrieve the name
                    instructor_name = filtered_instructor['name'] if filtered_instructor else None

                    context.update({
                        'sections': sections,
                        'instructor_name': instructor_name,
                    })
                return self.view.render_instructor_query(**context)
        except Exception as e:
            success, error = ErrorHandler.handle_controller(e)
            context.update({'success': success, 'error': error})

        return self.view.render_instructor_query(**context)

    def delete_instructor(self):
        success = True
        error = ''
        try:
            if request.method == 'POST':
                instructor_id = request.form.get('instructor_id', '').strip()
                print('Deleting instructor-steve {}'.format(instructor_id))

                if not instructor_id:
                    success = False
                    error = 'Please enter instructor ID'
                else:
                    self.model.delete_instructor(instructor_id)
                    return redirect(url_for('instructors'))

        except Exception as e:
            ErrorHandler.handle_controller(e)

        return redirect(url_for('instructors'))

