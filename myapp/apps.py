from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"

    def ready(self):
        # Import here to avoid circular imports
        # Only run this in the main process (not in management commands)
        import os
        if os.environ.get('RUN_MAIN', None) != 'true':
            try:
                # Log application startup without trying to call model_check_on_startup
                logger.info("Application starting up...")
            except Exception as e:
                logger.warning(f"Failed during startup: {e}")
