"""Provides the view of the widget."""
from apps.managers.score_mgr import score_mgr
import time
import threading
current_time = 0
time_length = 0

def supply(request, page_name):
    """Supply view_objects contents, which are the player name, team and points."""
    _ = page_name
    """threading.Timer(5,supply,[request,_])"""
    profile = request.user.get_profile()
    name = profile.name
    team = profile.team
    points = score_mgr.player_points(profile)
    time_now = time.time()
    
    return {
        "name": name,
        "team": team,
        "points": points,
        "time_now": time_now
    }

def update():
    threading.Timer(5,update)
    return time.time()
def startTimer(length):
    current_time = time.time()
    
def updateTimer():
    time_left = time_length - (time.time() - current_time) 
    return time_left

def currentTime():
    return {
        "time_now": time.time()
    }