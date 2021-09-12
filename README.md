# mockango
django-admin commands which generate fixture data for your given apps's models using Mimesis data generator
## installation
```shell
pip intall mockango
```
## usage
```shell
python manage.py generatedata <app_labels> --num <instance for each model> --format <fixture_file_format>
```
### example
```shell
python manage.py generatedata posts --num 5 --format yaml
```
