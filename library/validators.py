import datetime
from rest_framework.serializers import ValidationError

class PastDateTimeValidator:
    def __init__(self) -> None:
        pass
    
    def __call__(self, timestamp) -> None:
        if isinstance(timestamp, datetime.date):
            timestamp = datetime.datetime.combine(timestamp, datetime.time())

        if(timestamp > datetime.datetime.now()):
            raise ValidationError("The datetime must be in the past.")
        
    