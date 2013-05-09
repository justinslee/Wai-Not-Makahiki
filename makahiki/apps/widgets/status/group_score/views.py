"""Prepares the views for point scoreboard widget."""
from apps.widgets.scoreboard.views import remote_supply


def supply(request, page_name):
    """Supply the view_objects content for this widget, which is all the scoreboard data."""
    result = remote_supply(request, page_name)
    return result
