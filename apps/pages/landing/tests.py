from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from components.floors.models import Floor

class LandingFunctionalTestCase(TestCase):
  fixtures = ["base_floors.json"]
  
  def testLanding(self):
    """Check that we can load the landing page."""
    response = self.client.get(reverse("root_index"))
    self.failUnlessEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "landing/index.html")
    
  def testAboutRedirect(self):
    """Check that if a settings variable is set, then going to the root url goes to the about page."""
    current_setting = False
    if hasattr(settings, "REDIRECT_TO_ABOUT"):
      current_setting = settings.REDIRECT_TO_ABOUT
      
    settings.REDIRECT_TO_ABOUT = True
    response = self.client.get(reverse("root_index"), follow=True)
    self.failUnlessEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "landing/about.html")
    settings.REDIRECT_TO_ABOUT = current_setting
    
  def testLoggedInRedirect(self):
    """Tests that if the user is logged in, we redirect to the home page."""
    user = User.objects.create_user("user", "user@test.com", password="changeme")
    floor = Floor.objects.all()[0]
    profile = user.get_profile()
    profile.floor = floor
    profile.setup_complete = True
    profile.setup_profile = True
    profile.save()
    
    self.client.login(username="user", password="changeme")
    
    response = self.client.get(reverse("root_index"))
    self.assertRedirects(response, reverse("home_index"),
        msg_prefix="Landing page should redirect to home page for logged in users.")