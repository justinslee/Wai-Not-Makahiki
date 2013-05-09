"""Provides the view of the widget."""
from apps.managers.score_mgr import score_mgr


def supply(request, page_name):
    """Supply view_objects contents, which are the player name, team and points."""
    _ = page_name
    profile = request.user.get_profile()
    name = profile.name
    team = profile.team
    points = score_mgr.player_points(profile)
    return {
        "name": name,
        "team": team,
        "points": points,
    }

