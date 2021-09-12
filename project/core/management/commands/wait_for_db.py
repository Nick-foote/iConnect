import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psychopg2_Op_Error


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('\nwaiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except (OperationalError, Psychopg2_Op_Error):
                self.stdout.write('database unavailable, waiting one second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Connected to database'))