# view/degrees_view.py

from view.base_view import BaseView


# View for the Degrees Route
class DegreesView(BaseView):
    """View class for rendering the Degrees page, inherits from BaseView."""

    def render(self, degrees, selected_degree, courses, goals, sections):
        context = {
            'title': 'Degree Search',
            'subTitle': 'Degree Search',
            'degrees': degrees,
            'selected_degree': selected_degree,
            'courses': courses,
            'goals': goals,
            'sections': sections
        }

        return super().render('degrees.html', **context)
