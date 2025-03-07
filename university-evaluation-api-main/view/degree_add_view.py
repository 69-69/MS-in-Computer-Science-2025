# view/degrees_view.py

from view.base_view import BaseView


# View for the Degrees Route
class DegreeAddView(BaseView):
    """View class for rendering the Degrees page, inherits from BaseView."""

    def render(self, departments, courses, degreeLevels):
        context = {
            'title': 'Add Degree',
            'subTitle': 'Add Degree',
            'departments': departments,
            'courses': courses,
            'degreeLevels': degreeLevels
        }

        return super().render('degree_add.html', **context)
