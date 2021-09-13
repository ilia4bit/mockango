from random import randint
from django.db.models.fields import EmailField, URLField
from mimesis.schema import Field
from .constants import (INTEGER_FIELDS, BIG_INTEGER_FIELDS, SMALL_INTEGER_FIELDS, FLOAT_FIELDS,
                        DECIMAL_FIELDS, PK_FIELDS, PK_LIST_FIELDS, MAX_INTEGER, MAX_BIG_INTEGER, MAX_SMALL_INTEGER)
from .providers import AutoProvider, CharProvider, ChoicesProvider, ObjectProvider, TimeProvider


class BaseIdentifier:

    ALL_FIELDS = []

    def __init__(self, field, locale):
        self.field_name = field.name
        self.field_type = field.get_internal_type()
        try:
            self.field_choices = field.choices 
            self.field_default = field.default
            self.field_unique = field.unique
        except AttributeError:
            self.field_choices = None
            self.field_default = None
            self.field_unique = None
        self._ = Field(locale=locale, providers=[ChoicesProvider])

    def choice_field(self):
        return self._('choices.choices', items=self.field_choices)

    def generate(self):
        if self.field_choices:
            return self.choice_field()
        else:
            return self.generate_custom_field()

    def generate_custom_field(self):
        pass


class FieldNameIdentifier(BaseIdentifier):

    def __init__(self, field, locale):
        super().__init__(field, locale)

    def generate_custom_field(self):
        return self._(self.field_name)


class NumberIdentifier(BaseIdentifier):

    def __init__(self, field, locale, pk=None):
        super().__init__(field, locale)
        self._ = Field(locale=locale, providers=[
                       ChoicesProvider, AutoProvider])
        self.max_digits = field.max_digits if self.field_type in DECIMAL_FIELDS else 4
        self.start, self.end = self.set_start_and_end()
        self.pk = pk

    def set_start_and_end(self):
        if self.field_type in INTEGER_FIELDS:
            if self.field_type == 'PositiveIntegerField':
                return (0, MAX_INTEGER)
            return (-MAX_INTEGER - 1, MAX_INTEGER)
        elif self.field_type in BIG_INTEGER_FIELDS:
            if self.field_type == 'PositiveBigIntegerField':
                return (0, MAX_BIG_INTEGER)
            return (-MAX_BIG_INTEGER - 1, MAX_BIG_INTEGER)
        elif self.field_type in SMALL_INTEGER_FIELDS:
            if self.field_type == 'PositiveSmallIntegerField':
                return (0, MAX_SMALL_INTEGER)
            return (-MAX_SMALL_INTEGER - 1, MAX_SMALL_INTEGER)
        elif self.field_type in FLOAT_FIELDS:
            return (-1 * float(MAX_INTEGER) - 1.0, float(MAX_INTEGER))
        elif self.field_type in DECIMAL_FIELDS:
            decimal_range = '9'*self.max_digits
            return (-1 * float(decimal_range) - 1.0, float(decimal_range))
        else:
            return (0,0)

    def decimal_field(self):
        return self._('numbers.decimal_number', start=self.start, end=self.end)

    def float_field(self):
        return self._('numbers.float_number', start=self.start, end=self.end)

    def integer_field(self):
        if self.field_type in PK_FIELDS:
            return self._('auto.key', pk=self.pk)
        elif self.field_type in PK_LIST_FIELDS:
            return self._('auto.key_list', pk=self.pk)
        return self._('numbers.integer_number', start=self.start, end=self.end)

    def generate_custom_field(self):
        if self.field_type in [*INTEGER_FIELDS, *BIG_INTEGER_FIELDS, *SMALL_INTEGER_FIELDS, *PK_FIELDS, *PK_LIST_FIELDS]:
            return self.integer_field()
        elif self.field_type in DECIMAL_FIELDS:
            return self.decimal_field()
        elif self.field_type in FLOAT_FIELDS:
            return self.float_field()


class StringIdentifier(BaseIdentifier):

    def __init__(self, field, locale):
        super().__init__(field, locale)
        self._ = Field(locale=locale, providers=[ChoicesProvider, CharProvider])
        self.field_max_length = field.max_length if self.field_type != 'GenericIPAddressField' else None
        self.field_protocol = field.protocol if self.field_type == 'GenericIPAddressField' else None
        self.is_email = isinstance(field, EmailField)
        self.is_url = isinstance(field, URLField)

    def char_field(self):
        if self.is_email:
            return self._('person.email', unique=self.field_unique)
        elif self.is_url:
            return self._('char.url')
        return self._('random.randstr', length=self.field_max_length, unique=self.field_unique)

    def generic_ip_address_field(self):
        protocols = ['ip_v4', 'ip_v6']
        if self.field_protocol == 'IPv4':
            return self._('internet.ip_v4')
        elif self.field_protocol == 'IPv6':
            return self._('internet.ip_v4')
        # protocol == 'both'
        return self._(f'internet.{protocols[randint(0, 1)]}')

    def slug_field(self):
        return self._('char.slug', max_length=self.field_max_length)

    def text_field(self):
        return self._('text.text')

    def uuid_field(self):
        return self._('uuid')

    def generate_custom_field(self):
        if self.field_type == 'CharField':
            return self.char_field()
        elif self.field_type == 'GenericIPAddressField':
            return self.generic_ip_address_field()
        elif self.field_type == 'SlugField':
            return self.slug_field()
        elif self.field_type == 'TextField':
            return self.text_field()
        elif self.field_type == 'UUIDField':
            return self.uuid_field()


class BooleanIdentifier(BaseIdentifier):

    def boolean_field(self):
        return self._('development.boolean')

    def generate_custom_field(self):
        return self.boolean_field()


class TimeIdentifier(BaseIdentifier):


    def __init__(self, field, locale):
        super().__init__(field, locale)
        self._ = Field(locale=locale, providers=[
                       ChoicesProvider, TimeProvider])
        self.field_auto_now = field.auto_now if self.field_type in self.ALL_FIELDS[
            0:2] else None
        self.field_auto_now_add = field.auto_now_add if self.field_type in self.ALL_FIELDS[
            0:2] else None

    def date_field(self):
        if self.field_auto_now or self.field_auto_now_add:
            return self._('time.date')
        return self._('datetime.date')

    def date_time_field(self):
        if self.field_auto_now or self.field_auto_now_add:
            return self._('time.date_time')
        return self._('datetime.datetime')

    def duration_field(self):
        return self._('time.duration')
    
    def time_field(self):
        return self._('time.time')

    def generate_custom_field(self):
        if self.field_type == 'DateField':
            return self.date_field()
        elif self.field_type == 'DateTimeField':
            return self.date_time_field()
        elif self.field_type == 'DurationField':
            return self.duration_field()
        elif self.field_type == 'TimeField':
            return self.time_field()


class ObjectIdentifier(BaseIdentifier):

    def __init__(self, field, locale):
        super().__init__(field, locale)
        self._ = Field(locale=locale, providers=[ChoicesProvider, ObjectProvider])

    def json(self):
        return self._('object.json')

    def generate_custom_field(self):
        return self.json() 