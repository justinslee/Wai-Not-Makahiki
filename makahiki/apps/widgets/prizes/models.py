"""Implements the model for prize management."""
from django.db import models
from apps.managers.player_mgr import player_mgr
from apps.managers.resource_mgr import resource_mgr
from apps.managers.score_mgr import score_mgr

from apps.managers.team_mgr import team_mgr
from apps.managers.team_mgr.models import Group, Team
from apps.utils.utils import media_file_path
from apps.widgets.resource_goal import resource_goal
from apps.managers.challenge_mgr.models import RoundSetting


_MEDIA_LOCATION = "prizes"
"""location for uploaded files."""


class Prize(models.Model):
    """Represents a prize in the system."""
    AWARD_TO_CHOICES = (
        ("individual_overall", "Individual (Overall)"),
        ("individual_team", "Individual (Team)"),
        ("team_overall", " Team (Overall)"),
        ("team_group", " Team (Group)"),
        ("group_overall", "Group (Overall)"),
        )
    AWARD_CRITERIA_CHOICES = (
        ("points", "Points"),
        ("energy_usage", "Energy Usage"),
        ("energy_goal", "Energy Goal"),
        ("water_usage", "Water Usage"),
        ("water_goal", "Water Goal"),
        )

    round = models.ForeignKey(RoundSetting, null=True, blank=True,
                              help_text="The round of the prize")

    title = models.CharField(max_length=50, help_text="The title of the prize.")
    short_description = models.TextField(
        help_text="Short description of the prize. This should include information about who "
                  "can win it. It is usually displayed in the prize list page."
    )
    long_description = models.TextField(
        help_text="Detailed information about the prize. It is usually displayed in the details "
                  "view of the prize."
    )
    value = models.IntegerField(help_text="The value of the prize.")

    image = models.ImageField(
        max_length=1024,
        upload_to=media_file_path(_MEDIA_LOCATION),
        blank=True,
        help_text="A picture of the prize."
    )
    award_to = models.CharField(
        max_length=50,
        choices=AWARD_TO_CHOICES,
        help_text="The category of the award. This is used to calculated who or which team is "
                  "winning for which category."
    )
    competition_type = models.CharField(
        max_length=50,
        choices=AWARD_CRITERIA_CHOICES,
        help_text="The competition type of the award.")
    admin_tool_tip = "Prizes for the highest score"

    def __unicode__(self):
        if self.round == None:
            return "%s: %s" % (self.round, self.title)
        else:
            return "%s: %s" % (self.round.name, self.title)

    class Meta:
        """meta"""
        unique_together = ("round", "award_to", "competition_type")
        ordering = ("round__name", "award_to", "competition_type")

    def num_awarded(self, team=None):
        """Returns the number of prizes that will be awarded for this prize."""
        _ = team
        if self.award_to in ("individual_overall", "team_overall", "group"):
            # For overall prizes, it is only possible to award one.
            return 1

        elif self.award_to in ("team_group", "individual_group"):
            # For dorm prizes, this is just the number of groups.
            return Group.objects.count()

        elif self.award_to == "individual_team":
            # This is awarded to each team.
            return Team.objects.count()
        elif self.award_to == "group_overall":
            # This is awarded to each group.
            return score_mgr.group_awarded(score_mgr.group_points_leader())

        raise Exception("Unknown award_to value '%s'" % self.award_to)

    def leader(self, team=None):
        """Return the prize leader."""
        if self.round == None:
            round_name = "Round 1"
        else:
            round_name = self.round.name
        if self.competition_type == "points":
            return self._points_leader(team)
        elif self.competition_type == "energy":
            return resource_mgr.resource_leader("energy", round_name=round_name)
        elif self.competition_type == "energy_goal":
            return resource_goal.resource_goal_leader("energy", round_name=round_name)
        elif self.competition_type == "water":
            return resource_mgr.resource_leader("water", round_name=round_name)
        elif self.competition_type == "water_goal":
            return resource_goal.resource_goal_leader("water", round_name=round_name)

    def _points_leader(self, team=None):
        """Return the point leader."""
        if self.round == None:
            round_name = "Round 1"
        else:
            round_name = self.round.name
        if self.award_to == "individual_overall":
            return player_mgr.points_leader(round_name=round_name)

        elif self.award_to == "team_group":
            if team:
                leaders = team.group.team_points_leaders(num_results=1, round_name=round_name)
                if leaders:
                    return leaders[0]
            return None

        elif self.award_to == "team_overall":
            return team_mgr.team_points_leader(round_name=round_name)

        elif self.award_to == "individual_team":
            if team:
                leaders = team.points_leaders(num_results=1, round_name=round_name)
                if leaders:
                    return leaders[0]
            return None
        elif self.award_to == "group_overall":
            return score_mgr.group_points_leader()

        raise Exception("'%s' is not implemented yet." % self.award_to)
