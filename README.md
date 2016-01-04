[![Quantifiedcode](https://www.quantifiedcode.com/api/v1/project/5d4f4508cf1b402f8cc818aaed29546e/snapshot/origin:develop:HEAD/badge.svg)](https://www.quantifiedcode.com/app/project/5d4f4508cf1b402f8cc818aaed29546e)
[![Coverage Status](https://coveralls.io/repos/andela/limber/badge.svg?branch=develop&service=github)](https://coveralls.io/github/andela/limber?branch=develop)
[![Travis CI](https://travis-ci.org/andela/limber.svg?branch=develop)](https://travis-ci.org/andela/limber)

# [Limber](https://limber-staging.herokuapp.com)
A project management platform for Agile perfectionists with deadlines.

###Project dependencies###
- [Python](https://www.python.org/downloads/)
- [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html)
- [Postgresql](http://www.postgresql.org/download/)

###Setting up###

To run __Limber__ locally after installing the project dependencies, follow the following steps:

1 . Clone the repo and navigate to the project directory
```shell
$ git clone https://github.com/andela/limber.git && cd $_
```


2 . Activate a virtual environment
```shell
$ workon <env-name>
```


3 . Install the package dependencies
```shell
(<env-name>)$ pip install -r requirements.txt
```


4 . If all package dependencies install successfully, create [migrations](https://goo.gl/1kLUYj) for the project and apply them. Ensure you have the Postgres server running.
```shell
(<env-name>)$ python manage.py makemigrations
(<env-name>)$ python manage.py migrate
```  


5 . Start the server for the project
```shell
(<env-name>)$ python manage.py runserver
```

6 . Open http://127.0.0.1:8000 on your favorite web browser

####Running tests####

To run the project tests
```shell
(<env-name>)$ python manage.py test
```
