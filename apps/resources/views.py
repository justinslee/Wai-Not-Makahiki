import string

from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponse

from resources import DEFAULT_NUM_RESOURCES
from resources.models import Resource, Topic
from resources.forms import TopicSelectForm
# Create your views here.

def index(request):
  """Index page for the resources tab."""
  resources = None
  resource_count = 0
  view_all = request.GET.has_key("view_all") and request.GET["view_all"]
  view_all_url = None
  
  if request.GET.has_key("topics"):
    topic_form = TopicSelectForm(request.GET)
    if topic_form.is_valid():
      topics = topic_form.cleaned_data["topics"]
      if view_all:
        resources = Resource.objects.filter(topics__pk__in=topics).distinct().order_by("-created_at")
      else:
        resources = Resource.objects.filter(topics__pk__in=topics).distinct().order_by("-created_at")[0:DEFAULT_NUM_RESOURCES]
      resource_count = Resource.objects.filter(topics__pk__in=topics).distinct().count()
  
  else:
    # We get here on first load
    topic_form = TopicSelectForm() # Note that all topics are selected by default.
    if view_all:
      resources = Resource.objects.order_by("-created_at")
    else:
      resources = Resource.objects.order_by("-created_at")[0:DEFAULT_NUM_RESOURCES]
    resource_count = Resource.objects.count()

  # Create the list header and view all link.
  list_title = "%d resources"
  if not view_all and resource_count > DEFAULT_NUM_RESOURCES:
    view_all_url = _construct_all_url(request)
    list_title = list_title % DEFAULT_NUM_RESOURCES
  else:
    list_title = list_title % resource_count
    
  return render_to_response('resources/index.html', {
    "topic_form": topic_form,
    "resources": resources,
    "list_title": list_title,
    "resource_count": resource_count,
    "view_all_url": view_all_url,
  }, context_instance = RequestContext(request))
  
def _construct_all_url(request):
  """Constructs a view all url using the parameters in the request."""
  url = "/resources/view_all/"
  if request.GET.has_key("topics"):
    # If this url has topics, we need to append that list.
    url += "?" + request.GET.urlencode()
  
  return url
  
def filter(request):
  """Uses AJAX to update resources list."""
  view_all_url = None
  
  if request.is_ajax() and request.GET.has_key("topics"):
    topic_form = TopicSelectForm(request.GET)
    if topic_form.is_valid():
      topics = topic_form.cleaned_data["topics"]
      resources = Resource.objects.filter(topics__pk__in=topics).distinct().order_by("-created_at")[0:DEFAULT_NUM_RESOURCES]
      resource_count = Resource.objects.filter(topics__pk__in=topics).distinct().count()
      
      if resource_count > DEFAULT_NUM_RESOURCES:
        view_all_url = _construct_all_url(request)
      
      response = render_to_string("resources/list.html", {
        "resources": resources,
        "resource_count": resource_count,
        "view_all_url": view_all_url,
      })
      return HttpResponse(response, mimetype='text/plain')
  
  # If something goes wrong, all we can do is raise a 404 or 500.
  raise Http404
  
def view_all(request):
  """Uses AJAX to view all resources."""
  if request.is_ajax():
    if request.GET.has_key("topics"):
      topic_form = TopicSelectForm(request.GET)
      if topic_form.is_valid():
        topics = topic_form.cleaned_data["topics"]
        # Note that DEFAULT_NUM_RESOURCES is already loaded, so we just load the rest.
        resources = Resource.objects.filter(topics__pk__in=topics).distinct().order_by("-created_at")[DEFAULT_NUM_RESOURCES:]
        resource_count = Resource.objects.filter(topics__pk__in=topics).distinct().count()
    
    else:
      # View all on default page.
      resources = Resource.objects.order_by("-created_at")[DEFAULT_NUM_RESOURCES:]
      resource_count = Resource.objects.count()
      
    response = render_to_string("resources/list.html", {
      "resources": resources,
      "resource_count": resource_count,
    })
    return HttpResponse(response, mimetype='text/plain')
  
  # If something goes wrong, all we can do is raise a 404 or 500.
  raise Http404
  
def resource(request, resource_id):
  """View details for a resource."""
  resource = get_object_or_404(Resource, pk=resource_id)
  
  return render_to_response('resources/resource_detail.html', {
    "resource": resource,
  }, context_instance = RequestContext(request))