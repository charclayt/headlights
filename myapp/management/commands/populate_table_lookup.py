from django.core.management.base import BaseCommand
from django.apps import apps
from myapp.models import TableLookup

class Command(BaseCommand):
    help = "Populates the TableLookup table with all models."

    def handle(self, *args, **kwargs):
        # Get all models from the app
        for model in apps.get_models():
            table_name = model._meta.db_table
            _, created = TableLookup.objects.get_or_create(table_name=table_name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added table: {table_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Table {table_name} already exists"))
