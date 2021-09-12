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
```python
INSTALLED_APPS = [
  ...
  'mockango',
]
```
## usage
```app_labels```(positional):  labels of app you need fixture data for them

```--num```(optional)(default=10): number of object generate for each model

```--foramt```(optional)(default=yaml): format of fixture file

```--locale```(optional)(default=en): supported mimesis locales

```shell
python manage.py generatedata posts --num 5 --format yaml --locale fa
```
## examples
models.py
```python
class Post(models.Model):
  title = models.Charfield(max_length=200)
  text = models.TextField()
  is_publish = models.BooleanField(default=False)
  published_date = models.DateTimeField()
  CATEGORIES = [
    ('T', 'Tutorail'),
    ('N', 'Normal'),
    ]
  category = models.CharField(max_length=1, choices=CATEGORIES)
```
settings.py
```python
INSTALLED_APPS = [
  ...
  'mockango',
  'posts',
]
```
```shell
python manage.py generatedata posts --num 5
```
posts/fixture/post/fixture_file.yaml
```yaml
- fields:
    category: T
    is_publish: false
    published_date: 2018-02-21 05:29:26.253161
    text: Messages can be sent to and received from ports, but these messages must
      obey the so-called "port protocol." It is also a garbage-collected runtime system.
      Atoms can contain any character if they are enclosed within single quotes and
      an escape convention exists which allows any character to be used within an
      atom. The syntax {D1,D2,...,Dn} denotes a tuple whose arguments are D1, D2,
      ... Dn. Do you come here often?
    title: Messages can be sent to and received from ports, but these messages must
      obey the so-called "port protocol."
  model: posts.post
  pk: 1
- fields:
    category: N
    is_publish: false
    published_date: 2009-01-25 08:37:08.793574
    text: She spent her earliest years reading classic literature, and writing poetry.
      Do you have any idea why this is not working? Any element of a tuple can be
      accessed in constant time. Its main implementation is the Glasgow Haskell Compiler.
      Tuples are containers for a fixed number of Erlang data types.
    title: They are written as strings of consecutive alphanumeric characters, the
      first character being lowercase.
  model: posts.post
  pk: 2
- fields:
    category: T
    is_publish: false
    published_date: 2013-01-03 11:28:01.825650
    text: He looked inquisitively at his keyboard and wrote another sentence. Any
      element of a tuple can be accessed in constant time. Haskell is a standardized,
      general-purpose purely functional programming language, with non-strict semantics
      and strong static typing. Atoms are used within a program to denote distinguished
      values. Atoms can contain any character if they are enclosed within single quotes
      and an escape convention exists which allows any character to be used within
      an atom.
    title: They are written as strings of consecutive alphanumeric characters, the
      first character being lowercase.
  model: posts.post
  pk: 3
- fields:
    category: T
    is_publish: false
    published_date: 2006-06-24 11:19:25.527136
    text: Haskell features a type system with type inference and lazy evaluation.
      It is also a garbage-collected runtime system. Messages can be sent to and received
      from ports, but these messages must obey the so-called "port protocol." The
      sequential subset of Erlang supports eager evaluation, single assignment, and
      dynamic typing. Tuples are containers for a fixed number of Erlang data types.
    title: The syntax {D1,D2,...,Dn} denotes a tuple whose arguments are D1, D2, ...
      Dn.
  model: posts.post
  pk: 4
- fields:
    category: T
    is_publish: true
    published_date: 2006-10-17 12:10:48.115520
    text: Tuples are containers for a fixed number of Erlang data types. It is also
      a garbage-collected runtime system. He looked inquisitively at his keyboard
      and wrote another sentence. The Galactic Empire is nearing completion of the
      Death Star, a space station with the power to destroy entire planets. Messages
      can be sent to and received from ports, but these messages must obey the so-called
      "port protocol."
    title: Ports are created with the built-in function open_port.
  model: posts.post
  pk: 5
```
## If You Find It Useful
Hi my friend if you find mockango useful please give it one star or share with your friends.
I think it can be imporve it so if you find something missing make issue
**Thanks**
