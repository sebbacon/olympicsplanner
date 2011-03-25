import csv
import sys
import codecs
import locale
from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand

from app.models import Session
from app.models import Discipline
from app.models import Venue
from app.models import Event
from app.models import Price


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dry-run', '-n', dest='dry_run',
                    action="store_true",
                    help="Only show what would be done"),
        make_option('--quiet', '-q', dest='quiet',
                    action="store_true",
                    help="Be quiet about it"),
        make_option('--some-thing', '-s', dest='some_thing',
                    action="store",
                    help="Something"),
        )
    help = "Import events from a CSV"

    def handle(self, *args, **options):
        # make sure our print statements can handle unicode
        sys.stdout = codecs.getwriter(
            locale.getpreferredencoding())(sys.stdout)
        items = csv.reader(open(args[0], "r"))
        for day, session, medal_session, events_tuple, limit, venue, \
                prices_str, start_time, end_time in items:
            prices = []
            events = []
            for price in eval(prices_str):
                if price:
                    price = price[1:]
                    price_obj, _ = Price.objects.get_or_create(amount=price)
                    prices.append(price_obj)
            for gender, name in eval(events_tuple):
                if gender == "men":
                    gender = "m"
                elif gender == "women":
                    gender = "w"
                else:
                    gender = "b"
                event_obj, _ = Event.objects.get_or_create(name=name.strip(),
                                                           gender=gender)
                events.append(event_obj)
            starts = datetime.strptime("%s %s 2011" % (start_time, day),
                                       "%H:%M %B %d %Y")
            ends = datetime.strptime("%s %s 2011" % (end_time, day),
                                       "%H:%M %B %d %Y")
            venue, _ = Venue.objects.get_or_create(name=name)
            medal_session = eval(medal_session)
            limit = int(limit[len("Ticket Limit: "):])
            discipline, _ = Discipline.objects.get_or_create(name=session)
            sess, _ = Session.objects.get_or_create(
                discipline=discipline,
                starts=starts,
                ends=ends,
                medal_session=medal_session,
                limit=limit,
                venue=venue)
            for price in prices:
                sess.prices.add(price)
            for event in events:
                sess.events.add(event)
            print sess
                
