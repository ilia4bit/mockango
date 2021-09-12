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
## writer massage
Hey this is my first open source project it's not big but i think it is useful and i think i can imporve it so if you find something missing make issue thanks.

also if you find it useful share with your friend
## mockango limit
yet it's not support *database relation fields*, *incremental fields* but in future i will add it
mockango not good at generating big quantity of data but make job done!
fixture file format is yaml by default and other format like json, xml not supported yet

