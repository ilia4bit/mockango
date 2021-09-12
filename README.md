# mockango
django-admin commands which generate fixture data for your given apps's models using Mimesis data generator
## requirements
```shell
pip install django
pip install mimesis
pip install pyyaml
pip install colorama
```
## installation
```shell
pip intall mockango
```
## usage
```shell
python manage.py generatedata <app_labels> --num <instance for each model> --format <fixture_file_format> --locale <mimesis supported locale>
```
### example
```shell
python manage.py generatedata posts --num 5 --format yaml
```
