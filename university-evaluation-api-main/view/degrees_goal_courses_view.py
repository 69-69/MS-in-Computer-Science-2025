# view/degrees_goal_courses_view.py

from view.base_view import BaseView


class DegreesGoalCoursesView(BaseView):
    """View class for rendering the Degrees page, inherits from BaseView."""

    def render(self, goal, courses):
        context = {
            'title': 'Degree Goal Courses',
            'subTitle': 'Degree Goal Courses',
            'goal': goal,
            'courses': courses
        }

        return super().render('degrees_goal_courses.html', **context)
