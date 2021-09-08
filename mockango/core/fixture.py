import os
import json
import yaml
from datetime import datetime
from mimesis.schema import Schema, Field
from colorama import Fore


class Fixture:

    def __init__(self, model, num, fixture_format, locale):
        # self.model = model
        self.model_label = model._meta.label_lower
        self.model_name = model._meta.model_name
        self.model_fields = model._meta.get_fields()
        self.app_path = model._meta.app_config.path
        self.num = num
        self.fixture_format = fixture_format
        self.locale = locale
        self.model_fixture_dir_path = os.path.join(os.path.join(self.app_path, 'fixtures'), self.model_name)

    def field_provider_identifier(self, field):
        _ = Field(locale=self.locale)
        return _('text.word')

    def generate_objects(self):
        _ = Field(locale=self.locale)
        object_desc = (lambda: {'model': self.model_label, 'pk': self.field_provider_identifier(''), 'fields': {field.name: self.field_provider_identifier(field) for field in self.model_fields if field.name != 'id'}})
        schema = Schema(schema=object_desc)
        objects = schema.create(iterations=self.num)
        return objects

    def create_fixtures_dir(self):
        try:
            os.mkdir(self.model_fixture_dir_path)
            return Fore.CYAN + self.model_fixture_dir_path + Fore.GREEN + '\tCreated :)'
        except FileExistsError:
            return Fore.CYAN + self.model_fixture_dir_path + Fore.YELLOW + '\t Exist!'
        except FileNotFoundError:
            return Fore.CYAN + self.model_fixture_dir_path + Fore.RED + '\t Not Found :('

    def create_fixture_file(self):
        objects = self.generate_objects()
        fixture_file_name = '{}_mock_{}.{}'.format(self.model_name, datetime.now().strftime('%X').replace(':', '_'), self.fixture_format)
        try:
            with open(os.path.join(self.model_fixture_dir_path, fixture_file_name), mode='w') as ff:
                if self.fixture_format == 'yaml':
                    yaml.dump(objects, ff)
                else:
                    ff.write(json.dumps(objects))
            return Fore.CYAN + 'creating {}'.format(fixture_file_name) + Fore.GREEN + '\tGenerated :)'
        except FileExistsError:
            return Fore.CYAN + fixture_file_name + Fore.YELLOW + '\t Exist!'
        except FileNotFoundError:
            return Fore.CYAN + fixture_file_name + Fore.RED + '\t Not Found :('
