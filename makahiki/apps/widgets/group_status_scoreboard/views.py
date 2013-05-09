"""Prepares the views for point scoreboard widget."""
import datetime
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.player_mgr import player_mgr
from apps.managers.team_mgr import team_mgr


def supply(request, page_name):
    """Supply the view_objects content for this widget, which is all the scoreboard data."""

    user = request.user

    team = user.get_profile().team
    num_results = 10 if page_name != "status" else None
    round_standings = {}

    current_round = challenge_mgr.get_round_name()
    today = datetime.datetime.today()
    rounds = challenge_mgr.get_all_round_info()["rounds"]
    for key in rounds.keys():
        if rounds[key]["start"] <= today and \
            (rounds[key]["display_scoreboard"] or page_name == "status"):
            round_standings[key] = {
                "team_standings": team_mgr.team_points_leaders(num_results, key),
                "profile_standings": player_mgr.points_leaders(num_results, key),
                "team_participation": team_mgr.team_active_participation(num_results, key) if \
                                      page_name == "status" else None,
                "user_team_standings": team.points_leaders(num_results, key) if \
                                       team and page_name != "status" else None,
            }
    # add an overall scoreboard
    round_standings["Overall"] = {
        "team_standings": team_mgr.team_points_leaders(num_results, "Overall"),
        "profile_standings": player_mgr.points_leaders(num_results, "Overall"),
        "team_participation": team_mgr.team_active_participation(num_results, "Overall") if\
            page_name == "status" else None,
    }

    count = len(rounds)

    return {
        "profile": user.get_profile(),
        "team": team,
        "current_round": current_round,
        "round_standings": round_standings,
        "no_carousel": page_name == "status",
        "range": count,
        "user": user,
    }


def remote_supply(request, page_name):
    """Supplies data to remote views."""
    return supply(request, page_name)
