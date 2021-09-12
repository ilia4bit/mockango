import datetime
from random import randint
from django.utils import timezone
from mimesis.providers.base import BaseProvider


class ChoicesProvider(BaseProvider):

    class Meta:
        name = 'choices'
    
    @staticmethod
    def choices(items):
        return items[randint(0, len(items) - 1)][0]


class AutoProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__inc = 0

    class Meta:
        name = 'auto'

    def null():
        return None


class TimeProvider(BaseProvider):

    class Meta:
        name = 'time'

    @staticmethod
    def date():
        return datetime.date.today()
    
    @staticmethod
    def date_time():
        return timezone.now() 

    @staticmethod
    def duration():
        return datetime.timedelta.min