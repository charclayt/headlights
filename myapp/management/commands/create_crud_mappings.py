from django.core.management.base import BaseCommand
from myapp.models import OperationLookup

class Command(BaseCommand):
    help = "Create CRUD mappings for all models and store them in the OperationLookup table"

    def handle(self, *args, **kwargs):
        operations = ["Create", "Read", "Update", "Delete"]

        for operation in operations:
            # Ensure the operation is not duplicated
            _, created = OperationLookup.objects.get_or_create(operation_name=operation)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added operation: {operation}"))
            else:
                self.stdout.write(self.style.WARNING(f"Operation {operation} already exists"))
