"""Prepares the views for point scoreboard widget."""
import datetime
from apps.managers.resource_mgr import resource_mgr
from apps.widgets.resource_goal import resource_goal
from apps.managers.score_mgr import score_mgr
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr.models import ResourceUsage, ResourceSetting
from apps.managers.team_mgr.models import Team, Group

def supply(request, page_name):
    """Supply view_objects contents, which are the player name, team and points."""
    _ = page_name
    
    resources = {'energy','water','waste'}
    group_entries = {}

    today = datetime.datetime.today()

    for group in Group.objects.all():         
        temp = {}
        for resource in resources: 
            total = 0
            for team in Team.objects.all():
                if team.group.name == group.name: 
                    total = total + resource_mgr.team_resource_usage(today, team, resource)
            temp[resource] = total        
        group_entries[group] = temp;

    return {
        "group_entries": group_entries,
    }

