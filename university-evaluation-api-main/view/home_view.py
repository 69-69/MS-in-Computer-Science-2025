# view/home_view.py

from view.base_view import BaseView


# View class for rendering the Home page, inherits from BaseView.
class HomeView(BaseView):

    def render(self, success, error, evaluations):
        context = {
            'title': 'Degree Evaluation',
            'subTitle': '(CS7330 Group-11)',
            'success': success,
            'error': error,
            'evaluations': evaluations,
        }

        print(f"steven-courses:: {evaluations}")
        # Call the render method from the BaseView (Parent) class to render the 'index.html' template with the provided context (Data)
        return super().render('index.html', **context)
