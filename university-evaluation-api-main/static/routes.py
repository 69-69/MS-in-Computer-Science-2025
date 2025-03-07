# static/routes.py

from controller import controller

class Routes:
    @staticmethod
    def init_routes(app):
        # Create controller instances
        home_controller, degrees_controller, courses_controller, instructors_controller, evaluation_controller, departments_controller = controller()

        # Define the routes
        """
        Instead of defining a route with a separate 
        function for each controller (e.g., @app.route('/') def index()), 
        we can directly assign the controller methods to the routes. 
        """
        app.route('/', methods=['GET', 'POST'])(home_controller.index)
        app.route('/degrees', methods=['GET', 'POST'])(degrees_controller.degrees)
        app.route('/degrees/add', methods=['GET', 'POST'])(degrees_controller.degree_add)
        app.route('/degrees/goal/courses', methods=['GET'])(degrees_controller.degree_goal_courses)
        app.route('/courses', methods=['GET'])(courses_controller.courses)
        app.route('/add_course', methods=['POST'])(courses_controller.add_course)
        app.route('/add_section', methods=['POST'])(courses_controller.add_section)
        app.route('/get_course_sections', methods=['POST'])(courses_controller.get_course_sections)
        app.route('/add_goal', methods=['POST'])(evaluation_controller.add_goal)
        app.route('/evaluation', methods=['GET', 'POST'])(evaluation_controller.evaluation)
        app.route('/instructors', methods=['GET', 'POST'])(instructors_controller.instructors)
        app.route('/add_instructor', methods=['GET', 'POST'])(instructors_controller.add_instructor)
        app.route('/get_sections_status', methods=['POST'])(evaluation_controller.get_sections_status)
        app.route('/instructor_query', methods=['GET', 'POST'])(instructors_controller.instructor_query)
        app.route('/delete_instructor', methods=['GET', 'POST'])(instructors_controller.delete_instructor)
        app.route('/get_evaluation_sections', methods=['POST'])(evaluation_controller.get_evaluation_sections)
        app.route('/save_evaluation_data', methods=['POST'])(evaluation_controller.save_evaluation_data)
        app.route('/departments', methods=['GET', 'POST'])(departments_controller.departments)
        app.route('/add_department', methods=['GET', 'POST'])(departments_controller.add_department)