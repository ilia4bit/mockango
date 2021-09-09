from mimesis import schema
from colorama import Fore
from typing import Optional


class BaseGenerator:
    """
    all this options needed for other generator
    """

    def __init__(self, field, locale):
        self.internal_type = field.get_internal_type()
        self.name = field.name
        self.default = field.default
        self.choices = field.choices
        self.is_unique = field.unique
        self._ = schema.Field(locale=locale)

    def generate(self):
        return self._(self.name)


class NumberGenerator(BaseGenerator):
    """
    for django numeric fields
    the NumberGenerator result is mimesis.schema.Field
    NumberField check type of django numeric Fields and find best mimesis data provider for them
    """
    _INTEGER_FIELDS = ['BigIntegerField', 'IntegerField', 'PositiveBigIntegerField',
                       'PositiveIntegerField', 'PositiveSmallIntegerField', 'SmallIntegerField']
    _FLOAT_FIELDS = ['FloatField']
    _DECIMAL_FIELDS = ['DecimalField']
    ALL_VALID_FIELDS = [*_INTEGER_FIELDS, *_FLOAT_FIELDS, *_DECIMAL_FIELDS]

    def __init__(self, field, locale):
        super().__init__(field, locale)
        self.max_digits = field.max_digits if field.get_internal_type() == 'DecimalField' else None

    @staticmethod
    def get_min_and_max(internal_type, max_digits: Optional[int] = 4) -> tuple:
        if internal_type == 'BigIntegerField':
            return tuple([-92233720368547758078, 9223372036854775807])
        elif internal_type == 'DecimalField':
            max_val = float('9' * max_digits)
            min_val = -max_val
            return tuple([min_val, max_val])
        elif internal_type == 'PositiveBigIntegerField':
            return tuple([1, 9223372036854775807])
        elif internal_type == 'PositiveIntegerField':
            return tuple([1, 2147483647])
        elif internal_type == 'PositiveSmallIntegerField':
            return tuple([1, 32767])
        elif internal_type == 'SmallIntegerField':
            return tuple([-32768, 32767])
        elif internal_type == 'FloatField':
            return tuple([-2147483648.0, 2147483647.0])

        return tuple([-2147483648, 2147483647])

    def generate(self):
        if self.choices is not None:
            return self._('choice', self.choices)
        else:
            if self.internal_type in self._INTEGER_FIELDS:
                return self.integer()
            elif self.internal_type in self._FLOAT_FIELDS:
                return self.float()
            elif self.internal_type in self._DECIMAL_FIELDS:
                return self.decimal()

    def integer(self):
        start, end = self.get_min_and_max(self.internal_type, self.max_digits)
        return self._('numbers.integer_number', start=start, end=end)

    def float(self):
        start, end = self.get_min_and_max(self.internal_type, self.max_digits)
        return self._('numbers.float_number', start=start, end=end)

    def decimal(self):
        start, end = self.get_min_and_max(self.internal_type, self.max_digits)
        return self._('numbers.decimal_number', start=start, end=end)


class StringGenerator(BaseGenerator):
    """
    for django char based fields
    """
    ALL_VALID_FIELDS = ['CharField', 'EmailField', 'TextField']

    def __init__(self, field, locale):
        super().__init__(field, locale)
        self.max_length = field.max_length

    def generate(self):
        if self.choices is not None:
            return self._('choice', self.choices)
        else:
            if self.internal_type == 'CharField':
                return self.char()
            elif self.internal_type == 'EmailField':
                return self.email()
            elif self.internal_type == 'TextField':
                return self.text()

    def char(self):
        if self.is_unique:
            return self._('random.randstr', unique=True, length=self.max_length)
        return self._('random.randstr', length=self.max_length)

    def email(self):
        if self.is_unique:
            return self._('person.email', unique=True)
        return self._('person.email')

    def text(self):
        return self._('text.text', quantity=100)
