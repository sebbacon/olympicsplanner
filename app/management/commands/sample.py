import sys
import codecs
import locale
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

class Command(BaseCommand):
    option_list =  BaseCommand.option_list + (
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
        some_thing = options.get('some_thing', None)
        dry_run = options.get('dry_run', False)
        quiet = options.get('quiet', False)
        if not quiet:
            print "I am noisy"
