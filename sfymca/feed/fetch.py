from enum import Enum
import datetime
import logging

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests

from sfymca.feed.models import Branch, Event

logger = logging.getLogger(__name__)


PoolScheduleID = 110


class TableColumns(Enum):
    Event = 0
    Studio = 1
    TimeRange = 2
    Branch = 3


class FormFields(Enum):
    Branch = "field_location_reference_target_id[]"
    Date = "field_class_date_value[value][date]"
    ScheduleKind = "term_node_tid_depth[]"


IGNORED_EVENT_NAMES = [
    "group",
    "walking",
    "aerobics",
    "camp",
    "class",
    "lessons",
    "fit",
    "private",
]


def url_for_facility(branch, date):
    # Format date as MM/DD/YYYY
    url = (
        f"https://www.ymcasf.org/facility-schedule"
        f"?{FormFields.Branch.value}={branch.value}"
        f"&{FormFields.ScheduleKind.value}={PoolScheduleID}"
        f"&{FormFields.Date.value}={date:%m/%d/%Y}"
    )
    return url


def fetch_schedule(branch, date):
    url = url_for_facility(branch, date)

    logger.info(f"Fetching {url}")

    response = requests.get(url)
    response.raise_for_status()

    tree = BeautifulSoup(response.text, "html.parser")
    table = tree.find("table", class_="views-table")
    rows = table.find("tbody").find_all("tr")

    events = []

    for index, row in enumerate(rows):
        cols = row.find_all("td")

        name = cols[TableColumns.Event.value].text.strip()
        if any([n in name.lower() for n in IGNORED_EVENT_NAMES]):
            continue

        studio = cols[TableColumns.Studio.value].text.strip()
        if studio.lower() == "pool":
            studio = ""

        range_cell = cols[TableColumns.TimeRange.value]

        try:
            start_str = range_cell.find("span", class_="date-display-start")["content"]
        except TypeError:
            # Ensure there's a single entry, and if so, continue
            range_cell.find("span", class_="date-display-single")["content"]
            continue

        end_str = range_cell.find("span", class_="date-display-end")["content"]

        start, end = parse(start_str), parse(end_str)

        # For whatever reason, the tz offset has a bad offset...
        # tz = pytz.timezone('America/Los_Angeles')
        # start, end = start.replace(tzinfo=tz), end.replace(tzinfo=tz)

        if end < start:
            logger.warn("The end date was before the start date...")
            continue

        eid = f"{date:%Y-%m-%d}-{branch.value}-{studio}-{index}"

        events.append(Event(eid, name, branch, studio, start, end, url))

    return events


def fetch_next_days_for_branch(branch, days=7):
    today = datetime.date.today()
    dates = [today + datetime.timedelta(days=i) for i in range(0, days)]

    events = []

    for date in dates:
        events.extend(fetch_schedule(branch, date))

    # Sort the events by start time
    events.sort(key=lambda ev: ev.start)

    return events


def fetch_next_days(days=7):
    events = []

    for branch in Branch:
        events.extend(fetch_next_days_for_branch(branch, days))

    # Sort the events by start time
    events.sort(key=lambda ev: ev.start)

    return events
