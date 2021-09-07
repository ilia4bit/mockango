import os
import json
import yaml
from datetime import datetime
from colorama import Fore


class Fixture:

    def __init__(self, model, num, fixture_format, locale):
        self.model = model
        self.num = num
        self.fixture_format = fixture_format
        self.locale = locale
        self.fixtures_dir_path = os.path.join(model._meta.app_config.path, 'fixtures')

    def generate_objects(self):
        RELATION_FIELDS = {'pk': ['ForeignKey', 'OneToOneField'], 'pk_list': ['ManyToManyField']}
        for pk in range(1, self.num + 1):
            fields = {}
            for field in self.model._meta.get_fields():
                if field.name != 'id':
                    if field.get_internal_type() in RELATION_FIELDS['pk']:
                        fields[field.name] = pk
                    elif field.get_internal_type() in RELATION_FIELDS['pk_list']:
                        fields[field.name] = [pk]
                    else:
                        fields[field.name] = ''
            yield {
                "model": self.model._meta.model_name,
                "pk": pk,
                "fields": fields
            }

    def create_fixtures_dir(self):
        try:
            os.mkdir(self.fixtures_dir_path)
            return Fore.CYAN + self.fixtures_dir_path + Fore.GREEN + '\tCreated :)'
        except FileExistsError:
            return Fore.CYAN + self.fixtures_dir_path + Fore.YELLOW + '\t Exist!'
        except FileNotFoundError:
            return Fore.CYAN + self.fixtures_dir_path + Fore.RED + '\t Not Found :('

    def create_fixture_file(self):
        objects = list(self.generate_objects())
        fixture_file_name = '{}_mock_{}.{}'.format(self.model._meta.model_name, datetime.now().strftime('%X').replace(':', '_'), self.fixture_format)
        try:
            with open(os.path.join(self.fixtures_dir_path, fixture_file_name), mode='w') as ff:
                if self.fixture_format == 'yaml':
                    yaml.dump(objects, ff)
                else:
                    ff.write(json.dumps(objects))
            return Fore.CYAN + 'creating {}'.format(fixture_file_name) + Fore.GREEN + '\tDone :)'
        except FileExistsError:
            return Fore.CYAN + fixture_file_name + Fore.YELLOW + '\t Exist!'
        except FileNotFoundError:
            return Fore.CYAN + fixture_file_name + Fore.RED + '\t Not Found :('
