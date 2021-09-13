import datetime
from random import randint
from django.utils import timezone
from mimesis.providers.base import BaseProvider
from mimesis.random import Random


class ChoicesProvider(BaseProvider):

    class Meta:
        name = 'choices'

    @staticmethod
    def choices(items):
        return items[randint(0, len(items) - 1)][0]


class AutoProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        name = 'auto'

    @staticmethod
    def key(pk):
        return pk

    @staticmethod
    def key_list(pk):
        return [pk]


class TimeProvider(BaseProvider):

    class Meta:
        name = 'time'

    @staticmethod
    def date():
        return timezone.datetime.today()

    @staticmethod
    def date_time():
        return timezone.now()

    @staticmethod
    def duration():
        return timezone.timedelta.min

    @staticmethod 
    def time():
        return datetime.time.min


class CharProvider(BaseProvider):

    class Meta:
        name = 'char'

    @staticmethod
    def url():
        return 'https://github.com/iliark1382/mockango'

    @staticmethod
    def slug(max_length):
        length = max_length - len('mockango')
        return 'mockango-' + Random().randstr(unique=True, length=length) 
    


class ObjectProvider(BaseProvider):
     
    class Meta:
        name = 'object'
    
    @staticmethod
    def json():
        return {"use": "mockango"}