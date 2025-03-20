from datetime import datetime

class ErrorCodes:
    OK = 200
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500

class Views:
    HOME = "index"
    MACHINE_LEARNING = "ml_dashboard"

    API_MODELS_LIST = "api_models_list"
    API_UPLOAD_MODEL = "api_upload_model"

class Templates:
    HOME = "index.html"
    MACHINE_LEARNING = "ml/ml.html"

    LOGGED_OUT = "registration/logged_out.html"
    LOGIN = "registration/login.html"
    PASSWORD_RESET_COMPLETE = "registration/password_reset_complete.html"
    PASSWORD_RESET_CONFIRM = "registration/password_reset_confirm.html"
    PASSWORD_RESET_DONE = "registration/password_reset_done.html"
    PASSWORD_RESET_EMAIL = "registration/password_reset_email.html"
    PASSWORD_RESET_FORM = "registration/password_reset_form.html"

class TestData:
    EMAIL = "test@headlights.com"
    PHONE = "07123456789"
    ADDRESS = "123 Fake Street, Bristol, BS1 1BJ"
    NAME = "test name"
    VALUE = 8000
    PAST_DATE = datetime(year = 2020, month = 1, day = 1)
    PAST_DATETIME = datetime(year = 2020, month = 1, day = 1, hour = 0, minute = 0, second = 0)
    YEAR = 2020
    RATING = 5
