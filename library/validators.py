import datetime

from stdnum import isbn
from rest_framework.serializers import ValidationError


class PastDateTimeValidator:
    def __init__(self) -> None:
        pass

    def __call__(self, timestamp) -> None:
        # Convert potential date to datetime
        if isinstance(timestamp, datetime.date):
            timestamp = datetime.datetime.combine(timestamp, datetime.time())

        if timestamp > datetime.datetime.now():
            raise ValidationError("The datetime must be in the past.")


class ISBNValidator:
    def __init__(self) -> None:
        pass

    def __call__(self, raw_isbn):
        # Remove hyphens from the ISBN
        raw_isbn = raw_isbn.replace("-", "")

        if not isbn.is_valid(raw_isbn):
            raise ValidationError("Invalid ISBN.")
