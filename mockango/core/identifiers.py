from random import randint
from mimesis.schema import Field
from .providers import AutoProvider, ChoicesProvider, TimeProvider


class BaseIdentifier:

    ALL_FIELDS = []

    def __init__(self, field, locale):
        self.field_name = field.name
        self.field_choices = field.choices
        self.field_default = field.default
        self.field_type = field.get_internal_type()
        self.field_unique = field.unique
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

    # (end number,  list of field internal types)
    INTEGER_FIELDS = (
        2147483647, ('AutoField', 'IntegerField', 'PositiveIntegerField'))
    BIG_INTEGER_FIELDS = (922337203685477580, ('BigAutoField', 'BigIntegerField',
                          'PositiveBigIntegerField', 'ForeignKey', 'OneToOneField', 'ManyToManyField'))
    SMALL_INTEGER_FIElDS = (
        32767, ('SmallAutoField', 'SmallIntegerField', 'PositiveSmallIntegerField'))
    FLOAT_FIELDS = (2147483647.0, ['DecimalField', 'FloatField'])
    # used in Fixture Class
    ALL_FIELDS = [*INTEGER_FIELDS[1], *BIG_INTEGER_FIELDS[1],
                  *SMALL_INTEGER_FIElDS[1], *FLOAT_FIELDS[1]]

    def __init__(self, field, locale):
        super().__init__(field, locale)
        self._ = Field(locale=locale, providers=[ChoicesProvider, AutoProvider])
        self.max_digits = field.max_digits if self.field_type == 'DecimalField' else 4
        self.start, self.end = self.set_start_and_end()

    def set_start_and_end(self):
        if self.field_type in self.INTEGER_FIELDS[1]:
            if self.field_type == 'PositiveIntegerField':
                return (0, self.SMALL_INTEGER_FIElDS[0])
            return (-self.INTEGER_FIELDS[0] - 1, self.INTEGER_FIELDS[0])
        elif self.field_type in self.BIG_INTEGER_FIELDS[1]:
            if self.field_type == 'PositiveBigIntegerField':
                return (0, self.SMALL_INTEGER_FIElDS[0])
            return (-self.BIG_INTEGER_FIELDS[0] - 1, self.BIG_INTEGER_FIELDS[0])
        elif self.field_type in self.SMALL_INTEGER_FIElDS[1]:
            if self.field_type == 'PositiveSmallIntegerField':
                return (0, self.SMALL_INTEGER_FIElDS[0])
            return (-self.SMALL_INTEGER_FIElDS[0] - 1, self.SMALL_INTEGER_FIElDS[0])
        elif self.field_type in self.FLOAT_FIELDS[1]:
            return (-self.FLOAT_FIELDS[0] - 1, self.FLOAT_FIELDS[0])

    def decimal_field(self):
        return self._('numbers.decimal_number', start=self.start, end=self.end)

    def float_field(self):
        return self._('numbers.float_number', start=self.start, end=self.end)

    def integer_field(self):
        if self.field_type in ['AutoField', 'BigAutoField', 'SmallAutoField', 'ForeignKey', 'OneToOneField', 'ManyToManyField']:
            return self._('auto.null')
        return self._('numbers.integer_number', start=self.start, end=self.end)

    def generate_custom_field(self):
        if self.field_type in [*self.INTEGER_FIELDS[1], *self.BIG_INTEGER_FIELDS[1], *self.SMALL_INTEGER_FIElDS[1]]:
            return self.integer_field()
        if self.field_type in [*self.FLOAT_FIELDS[1]]:
            if self.field_type == self.FLOAT_FIELDS[1][0]:
                return self.decimal_field()
            else:
                return self.float_field()


class StringIdentifier(BaseIdentifier):

    ALL_FIELDS = ['CharField', 'EmailField',
                  'GenericIPAddressField', 'SlugField', 'TextField']

    def __init__(self, field, locale):
        super().__init__(field, locale)
        self.field_max_length = field.max_length if self.field_type != 'GenericIPAddressField' else None
        self.field_protocol = field.protocol if self.field_type == 'GenericIPAddressField' else None

    def char_field(self):
        return self._('random.randstr', length=self.field_max_length, unique=self.field_unique)

    def email_field(self):
        return self._('person.email', unique=self.field_unique, locale=self.locale)

    def generic_ip_address_field(self):
        protocols = ['ip_v4', 'ip_v6']
        if self.field_protocol == 'IPv4':
            return self._('internet.ip_v4')
        elif self.field_protocol == 'IPv6':
            return self._('internet.ip_v4')
        # protocol == 'both'
        return self._(f'internet.{protocols[randint(0, 1)]}')

    def slug_field(self):
        return self._('internet.slug')

    def text_field(self):
        return self._('text.text')

    def generate_custom_field(self):
        if self.field_type == 'CharField':
            return self.char_field()
        elif self.field_type == 'EmailField':
            return self.email_field()
        elif self.field_type == 'GenericIPAddressField':
            return self.generic_ip_address_field()
        elif self.field_type == 'SlugField':
            return self.slug_field()
        elif self.field_type == 'TextField':
            return self.text_field()


class BooleanIdentifier(BaseIdentifier):

    ALL_FIELDS = ['BooleanField']

    def boolean_field(self):
        return self._('development.boolean')
    
    def generate_custom_field(self):
        return self.boolean_field()


class TimeIdentifier(BaseIdentifier):
    
    ALL_FIELDS = ['DateField', 'DateTimeField', 'DurationField']

    def __init__(self, field, locale):
        super().__init__(field, locale)
        self._ = Field(locale=locale, providers=[ChoicesProvider, TimeProvider])
        self.field_auto_now = field.auto_now if self.field_type in self.ALL_FIELDS[0:2] else None
        self.field_auto_now_add = field.auto_now_add if self.field_type in self.ALL_FIELDS[0:2] else None

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

    def generate_custom_field(self):
        if self.field_type == 'DateField':
            return self.date_field()
        elif self.field_type == 'DateTimeField':
            return self.date_time_field()
        elif self.field_type == 'DurationField':
            return self.duration_field()
