import datetime
import pytz
from rest_framework.serializers import ValidationError

class PastDateTime:
    def __init__(self) -> None:
        pass
    
    def __call__(self, timestamp) -> None:
        # TODO: This is probably wrong... Look at the docs
        if isinstance(timestamp, datetime.date):
            timestamp = datetime.datetime.combine(timestamp, datetime.time())
            tz = pytz.timezone("Europe/Prague")
            timestamp = tz.localize(timestamp)

        if(timestamp > datetime.datetime.now(pytz.timezone("Europe/Prague"))):
            raise ValidationError("The datetime must be in the past.")
        
    