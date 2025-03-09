from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError

class DatabaseTest(TestCase):  

    def test_database_connection(self):
        db_conn = connections['default']

        self.assertTrue(db_conn, "Database connection exists")
        self.assertTrue(db_conn.cursor(), "Database cursor exists")
