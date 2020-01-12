from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from sfymca.feed.calendar import calendar_for_events
from sfymca.feed.fetch import fetch_next_days


class Command(BaseCommand):
    help = "Load events from SF YMCA"

    def handle(self, *args, **options):
        events = self._fetch_schedule(1)

        self._handle_response(events)

    def _fetch_schedule(self, days):
        try:
            return fetch_next_days(days)
        except Exception as e:
            raise CommandError(f"{e}")

    def _handle_response(self, events):
        cal = calendar_for_events(events)
        self.stdout.write(str(cal))

        self.stdout.write(self.style.SUCCESS("done"))
