from managers.team_mgr.models import Dorm, Floor
from widgets.energy.models import FloorEnergyGoal
from managers.player_mgr.models import Profile

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from managers.team_mgr.models import Floor
from widgets.energy.models import FloorEnergyGoal
import unittest

class EnergyFunctionalTestCase(TestCase):
    fixtures = ["base_floors.json"]

    def setUp(self):
        """Initialize a user and log them in."""
        self.user = User.objects.create_user("user", "user@test.com", password="changeme")
        self.floor = Floor.objects.all()[0]
        profile = self.user.get_profile()
        profile.floor = self.floor
        profile.setup_complete = True
        profile.setup_profile = True
        profile.save()

        self.client.login(username="user", password="changeme")

    def testIndex(self):
        """Check that we can load the index page."""
        response = self.client.get(reverse("energy_index"))
        self.failUnlessEqual(response.status_code, 200)

    def testEnergyScoreboard(self):
        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["energy"]["goals_scoreboard"]
        for goal in goals:
            self.assertEqual(goal["completions"], 0, "No floor should have completed a goal.")

        goal = FloorEnergyGoal.objects.create(
            floor=self.floor,
            goal_usage="1.0",
            actual_usage="2.0",
        )

        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["energy"]["goals_scoreboard"]
        for goal in goals:
            self.assertEqual(goal["completions"], 0, "No floor should have completed a goal.")

        goal = FloorEnergyGoal.objects.create(
            floor=self.floor,
            goal_usage="1.0",
            actual_usage="0.5",
        )

        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["energy"]["goals_scoreboard"]
        for floor in goals:
            if floor["floor__number"] == self.floor.number and floor["floor__dorm__name"] == self.floor.dorm.name:
                # print floor.floorenergygoal_set.all()
                self.assertEqual(floor["completions"], 1,
                    "User's floor should have completed 1 goal, but completed %d" % floor["completions"])
            else:
                self.assertEqual(floor["completions"], 0, "No floor should have completed a goal.")

class FloorEnergyGoalTest(TestCase):
  def setUp(self):
    dorm = Dorm.objects.create(name="Test Dorm")
    dorm.save()
    self.floor = Floor.objects.create(
        dorm=dorm,
        number="A"
    )
    
    self.user = User.objects.create_user("user", "user@test.com")
    profile = self.user.get_profile()
    profile.floor = self.floor
    profile.save()
    
  def testFloorEnergyGoal(self):
    profile = self.user.get_profile()
    points = profile.points
    
    goal = FloorEnergyGoal(
        floor=self.floor, 
        goal_usage=str(1.0), 
        actual_usage=str(0.5),
    )
    goal.save()
    profile = Profile.objects.get(user__username="user")
    self.assertEqual(profile.points, points, 
        "User that did not complete the setup process should not be awarded points.")
    
    profile.setup_complete = True
    profile.save()
    
    goal.actual_usage = "1.5"
    goal.save()
    profile = Profile.objects.get(user__username="user")
    self.assertEqual(profile.points, points, 
        "Floor that failed the goal should not be awarded any points.")
        
    goal.actual_usage = "0.5"
    goal.save()
    profile = Profile.objects.get(user__username="user")
    self.assertEqual(profile.points, points + FloorEnergyGoal.GOAL_POINTS,
        "User that setup their profile should be awarded points.")
    
    
    
