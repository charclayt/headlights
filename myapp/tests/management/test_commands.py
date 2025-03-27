from django.apps import apps
from django.core.management import call_command
from django.test import TestCase

from myapp.models import OperationLookup, TableLookup

from io import StringIO

class CreateCRUDMappingsTestCase(TestCase):
    def setUp(self):
        OperationLookup.objects.all().delete()

    def test_command_creates_operations(self):
        """Test that the command creates CRUD operations if they do not exist."""
        out = StringIO()
        call_command("create_crud_mappings", stdout=out)
        
        # Check that all CRUD operations are created
        operations = list(OperationLookup.objects.values_list("operation_name", flat=True))
        expected_operations = ["Create", "Read", "Update", "Delete"]
        
        self.assertCountEqual(operations, expected_operations)
        
        # Check output
        for operation in expected_operations:
            self.assertIn(f"Added operation: {operation}", out.getvalue())
    
    def test_command_does_not_duplicate_operations(self):
        """Test that running the command multiple times does not duplicate entries."""
        # Pre-populate the database
        OperationLookup.objects.bulk_create([
            OperationLookup(operation_name="Create"),
            OperationLookup(operation_name="Read"),
            OperationLookup(operation_name="Update"),
            OperationLookup(operation_name="Delete"),
        ])
        
        out = StringIO()
        call_command("create_crud_mappings", stdout=out)
        
        # Ensure no new operations were added
        self.assertEqual(OperationLookup.objects.count(), 4)
        
        # Check the output messages for warnings instead of success messages
        for operation in ["Create", "Read", "Update", "Delete"]:
            self.assertIn(f"Operation {operation} already exists", out.getvalue())

class PopulateTableLookupTestCase(TestCase):
    def setUp(self):
        TableLookup.objects.all().delete()

    def test_command_creates_table_entries(self):
        """Test that the command correctly populates TableLookup with all models."""
        out = StringIO()
        call_command("populate_table_lookup", stdout=out)
        
        # Get all expected table names from models
        expected_tables = [model._meta.db_table for model in apps.get_models()]
        stored_tables = list(TableLookup.objects.values_list("table_name", flat=True))
        
        self.assertCountEqual(stored_tables, expected_tables)
        
        # Check the output messages
        for table in expected_tables:
            self.assertIn(f"Added table: {table}", out.getvalue())
    
    def test_command_does_not_duplicate_entries(self):
        """Test that running the command multiple times does not create duplicates."""
        # Pre-populate the TableLookup table
        TableLookup.objects.bulk_create([
            TableLookup(table_name=model._meta.db_table) for model in apps.get_models()
        ])
        
        out = StringIO()
        call_command("populate_table_lookup", stdout=out)
        
        # Ensure no new table entries were added
        self.assertEqual(TableLookup.objects.count(), len(apps.get_models()))
        
        # Check the output messages for warnings instead of success messages
        for table in [model._meta.db_table for model in apps.get_models()]:
            self.assertIn(f"Table {table} already exists", out.getvalue())
