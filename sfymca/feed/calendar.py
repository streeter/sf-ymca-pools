import re

from ics import Calendar, Event

from .fetch import url_for_facility, fetch_next_days_for_branch


def calendar_event_for_event(branch, event):
    return Event(
        name=event.name,
        begin=event.start,
        end=event.end,
        uid=event.eid,
        location=event.location,
        url=event.url,
    )


def calendar_for_branch(branch):
    events = fetch_next_days_for_branch(branch)

    cal_events = [calendar_event_for_event(branch, e) for e in events]

    cal = Calendar(events=cal_events, creator="sfymca")
    cal.method = "PUBLISH"
    cal.scale = "GREGORIAN"

    lines = str(cal).split("\r\n")
    indicies = [i for i, s in enumerate(lines) if s.startswith("BEGIN:")]

    if len(indicies) > 1:
        second_index = indicies[1]
        lines.insert(second_index, f"X-WR-CALNAME:{branch.name} YMCA Pool")
        lines.insert(second_index + 1, "X-WR-TIMEZONE:America/Los_Angeles")

    return "\r\n".join(lines)


def calendar_for_events(events):
    cal_events = [
        Event(name=e.name, begin=e.start, end=e.end, uid=e.id) for e in events
    ]

    return Calendar(events=cal_events)
