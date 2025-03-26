from django.db.models.signals import post_save, post_delete
from django.db import models, transaction

from django.dispatch import receiver
from django.utils.timezone import now
from django.apps import apps

from myapp.middleware import get_current_user
from myapp.models import DatabaseLog, OperationLookup, TableLookup, UserProfile

from threading import local
import logging

logging = logging.getLogger(__name__)
local = local()

def prevent_recursion():
    """Prevent recursion by checking if the signal is already handled."""
    return getattr(local, "in_signal", False)

def set_in_signal(value):
    """Set the flag indicating that the signal is being processed."""
    local.in_signal = value

@receiver(post_save)
def log_create_or_update(sender, instance, created, **kwargs):
    """Logs create and update operations for all models."""

    if prevent_recursion():
        return

    set_in_signal(True)

    try:
        operation_id = 1 if created else 3
        user = get_current_user()
        user_profile = UserProfile.objects.get(auth_id=user)
    
        with transaction.atomic():
            DatabaseLog.objects.create(
            log_time=now(),
            user_id=user_profile,
            affected_table_id=TableLookup.objects.get(table_name=sender.__name__),
            operation_performed=OperationLookup.objects.get(pk=operation_id),
            successful=True
    )
    except Exception as e:
        logging.warning('failed to save logging to DB')
        logging.warning(f"{e}")
    finally:
        set_in_signal(False)

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    """Logs delete operations for all models."""
    if prevent_recursion():
        return

    set_in_signal(True)

    try:
        operation_id = 4
        user = get_current_user()
        user_profile = UserProfile.objects.get(auth_id=user)

        with transaction.atomic():
            DatabaseLog.objects.create(
                log_time=now(),
                user_id=user_profile,  
                affected_table_id=TableLookup.objects.get(table_name=sender.__name__),
                operation_performed=OperationLookup.objects.get(pk=operation_id),
                successful=True
            )
    except Exception as e:
        logging.warning('failed to save logging to DB')
        logging.warning(f"{e}")
    finally:
        set_in_signal(False)
