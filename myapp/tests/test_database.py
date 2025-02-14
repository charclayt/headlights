from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError


class DatabaseTest(TestCase):
    def test_database_connection(self):
        db_conn = connections['default']

        try:
            db_conn.cursor()
        except OperationalError:
            self.fail("Database connection failed")
        else:
            self.assertTrue(True, "Database connection succeeded")
