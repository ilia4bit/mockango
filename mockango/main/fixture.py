import os
import yaml
from mimesis.exceptions import UnsupportedField
from mimesis.providers import Generic
from colorama import Fore
from .identifiers import FieldNameIdentifier, NumberIdentifier, ObjectIdentifier, StringIdentifier, BooleanIdentifier, TimeIdentifier
from .constants import ALL_NUMBER_FIELDS, ALL_CHAR_FIELDS, ALL_BOOL_FIELDS, ALL_TIME_FIELDS, ALL_OBJECT_FIELDS


class Fixture:

    def __init__(self, model, num, fixture_format, locale):
        self.model_label = model._meta.label_lower
        self.model_name = model._meta.model_name
        self.model_fields = model._meta.get_fields()
        self.num = num
        self.fixture_format = fixture_format
        self.locale = locale
        self.model_fixture_dir_path = os.path.join(os.path.join(model._meta.app_config.path, 'fixtures'), self.model_name)
    
    def field_identifier(self, field, pk):
        try:
            return FieldNameIdentifier(field=field, locale=self.locale).generate()
        except UnsupportedField:
            if field.get_internal_type() in ALL_NUMBER_FIELDS: 
                return NumberIdentifier(field=field, locale=self.locale, pk=pk).generate()
            elif field.get_internal_type() in ALL_CHAR_FIELDS: 
                return StringIdentifier(field=field, locale=self.locale).generate()
            elif field.get_internal_type() in ALL_BOOL_FIELDS: 
                return BooleanIdentifier(field=field, locale=self.locale).generate()
            elif field.get_internal_type() in ALL_TIME_FIELDS: 
                return TimeIdentifier(field=field, locale=self.locale).generate()
            elif field.get_internal_type() in ALL_OBJECT_FIELDS:
                return ObjectIdentifier(field=field, locale=self.locale).generate()


    def generate_objects(self):
        for pk in range(1, self.num + 1):
            obj = {'model': self.model_label, 'pk': pk, 'fields': {field.name: self.field_identifier(field, pk) for field in self.model_fields if field.name != 'id'}}
            yield obj 

    def create_model_fixture_dir(self):
        try:
            os.mkdir(self.model_fixture_dir_path)
            return Fore.WHITE + self.model_fixture_dir_path + Fore.GREEN + '\tCreated :)'
        except FileExistsError:
            return Fore.WHITE + self.model_fixture_dir_path + Fore.YELLOW + '\tExist :|'
        except FileNotFoundError:
            return Fore.WHITE + self.model_fixture_dir_path + Fore.RED + '\tNot Found :('
            
    def create_model_fixture_file(self):
        objects = list(self.generate_objects())
        fixture_file_name = f'{Generic().cryptographic.uuid()}.{self.fixture_format}'
        fixture_file_path = os.path.join(self.model_fixture_dir_path, fixture_file_name)
        try:
            with open(fixture_file_path, mode='w') as fixture_file:
                yaml.dump(objects, stream=fixture_file)
                return Fore.WHITE + fixture_file_name + Fore.GREEN + '\tCreated :)'
        except FileExistsError:
            return Fore.WHITE + fixture_file_name + Fore.YELLOW + '\tExist :|'
        except FileNotFoundError:
            return Fore.WHITE + fixture_file_name + Fore.RED + '\tNot Found :('
