from flask import request, flash
from view.degrees_view import DegreesView
from view.degrees_goal_courses_view import DegreesGoalCoursesView
from view.degree_add_view import DegreeAddView
from model.db_model import DBModel
from static.error_handler import ErrorHandler
from datetime import datetime

class DegreesController:
    def __init__(self):
        self.model = DBModel()
        self.view = DegreesView()
        self.view_goal = DegreesGoalCoursesView()
        self.view_add = DegreeAddView()
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

    def get_selected_degree_sections(self, name, level):
        if request.form.get('request-type') != 'section_search':
            return None

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
            flash('You must select a beining year and semester that is not after the ending year and semester.')
            return None


        section_results = self.model.get_degree_sections(name, level, beginning_year_semester, ending_year_semester)

        return section_results

    def get_selected_degree_data(self):
        if request.method != 'POST':
            return None, None, None, None
        degree_selectin = request.form.get('degree-selection')
        if degree_selectin == '':
            if request.form.get('request-type') == 'open_degree':
                flash('A degree must be selected before opening it.', 'error')
            return None, None, None, None
        degree_name, degree_level = degree_selectin.split('<<>>')
        degree_results = self.model.get_degree(degree_name, degree_level)

        if not degree_results or len(degree_results) == 0:
            flash(f'No degree found with the name "{degree_name}" and level "{degree_level}"', 'error')
            return None, None, None, None

        course_results = self.model.get_degree_courses(degree_name, degree_level)
        goal_results = self.model.get_degree_goals(degree_name, degree_level)
        section_results = self.get_selected_degree_sections(degree_name, degree_level)
        return degree_results[0], course_results, goal_results, section_results


    def degrees(self):
        degrees = self.model.get_all_degrees()
        selected_degree, courses, goals, sections = self.get_selected_degree_data()

        return self.view.render(degrees, selected_degree, courses, goals, sections)

    def degree_goal_courses(self):
        goal_code = request.args.get('goal_code')
        degree_name = request.args.get('degree_name')
        degree_level = request.args.get('degree_level')
        if any(not self.string_exists(element) for element in [degree_name, degree_level, goal_code]):
            flash('Must have goal code, degree name, and degree level to find associated courses', 'error')
            return self.view_goal.render(None, None)

        goal_results = self.model.get_degree_goal(goal_code, degree_name, degree_level);
        if not goal_results or len(goal_results) == 0:
            flash(f'No goal found with code "{goal_code}", degree name "{degree_name}", and degree level "{degree_level}"', 'error')
            return self.view_goal.render(None, None)

        goal_courses = self.model.get_degree_goal_courses(goal_code)
        if not goal_courses or len(goal_courses) == 0:
            flash('No courses found for this goal', 'error')
        
        return self.view_goal.render(goal_results[0], goal_courses)

    def degree_add(self):
        if request.method == 'POST':
            request_type = request.form.get('request-type')
            if request_type =='add_degree':
                degree_name = request.form.get('degree_name')
                degree_level = request.form.get('degree_level')
                department_name = request.form.get('department_name')
                if all(self.string_exists(element) for element in [degree_name, degree_level, department_name]):
                    count = 0
                    degree_courses = []
                    while True:
                        count += 1
                        course_number = request.form.get(f'course_number_{count}')
                        if not self.string_exists(course_number):
                            break
                        is_core = request.form.get(f'course_is_core_{count}') == 'on'
                        degree_courses.append({
                            'course_number': course_number,
                            'is_core': is_core
                        })
                    if self.model.insert_degree(degree_name, degree_level, department_name, degree_courses):
                        flash(f'degree "{degree_name}" successfully added', 'success')

                else:
                    flash('Degree name, level, and department are required.', 'error')
            if request_type == 'add_level':
                new_level = request.form.get('new_level')
                if self.string_exists(new_level):
                    if self.model.insert_degree_level(new_level):
                        flash(f'degree level "{new_level}" successfully added', 'success')
                else:
                    flash('You must enter a new degree level to add it.', 'error')
        departments = self.model.get_all_departments()
        courses = self.model.get_all_courses()
        degree_levels = self.model.get_all_degree_levels()


        return self.view_add.render(departments, courses, degree_levels)

