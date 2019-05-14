from ics import Calendar, Event


def calendar_for_events(events):
    cal_events = [
        Event(name=e.name, begin=e.start, end=e.end, uid=e.id)
        for e in events
    ]

    return Calendar(events=cal_events)
