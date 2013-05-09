"""Provides the view of the widget."""
from apps.widgets.water_app.models import ApSel, Question
profile = 0

def supply(request, page_name):
    _ = page_name
    profile = request.user.get_profile()
    location = 0
    questions = Question.objects.order_by('?')[0]
    return {
        "location": location,
        "questions": questions,
    }
    
def getSetting():
    entry = ApSel.objects.all()
    if entry:
        return entry[0]
    else:
        return 0
    