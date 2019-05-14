from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from .calendar import calendar_for_events
from .fetch import fetch_next_days_for_branch
from .models import Branch


@cache_control(max_age=60*60*24, public=True)
def index(request):
    branches = [b.name.lower() for b in Branch]
    return render(
        request,
        "index.html",
        {"branches": branches},
    )


@cache_control(max_age=60*60, public=True)
def branch(request, branch_name):
    try:
        branch = [
            b for b in Branch
            if b.name.lower() == branch_name
        ][0]
    except IndexError:
        raise Http404('Branch does not exist')

    events = fetch_next_days_for_branch(branch)

    calendar = calendar_for_events(events)

    response = HttpResponse(
        str(calendar),
        content_type="text/calendar")
    response['Content-Disposition'] = f'attachment; filename="{branch_name}.ics"'
    return response
