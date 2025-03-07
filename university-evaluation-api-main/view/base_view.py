# view/base_view.py

class BaseView:
    """Base render method to be overridden by subclasses."""

    def render(self, template_name, **context):

        from flask import render_template, request

        # Get the current URL or route name
        current_url = request.path or None
        if current_url is None:
            current_url = request.referrer

        # Optionally, set any other context variables
        context['header'] = 'header.html'
        context['footer'] = 'footer.html'
        context['current_url'] = current_url

        # Render the template with the provided context
        return render_template(template_name, **context)
