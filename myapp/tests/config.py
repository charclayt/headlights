from datetime import datetime

class ErrorCodes:
    OK = 200
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500

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
