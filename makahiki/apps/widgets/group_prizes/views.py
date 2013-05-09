"""Prepares the views for point scoreboard widget."""
import datetime

from apps.managers.score_mgr import score_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal import resource_goal
from apps.managers.team_mgr.models import Team, Group

def supply(request, page_name):
    """Supply view_objects contents, which are the player name, team and points."""
    """Supply the view_objects content."""
    _ = request
    group_winner = score_mgr.group_points_leader()
    

    return {
            'group_winner':group_winner}
#view_objects

