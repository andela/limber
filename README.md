# Limber
A project management platform for Agile perfectionists with deadlines.

###Project dependencies###
- Git
- Python
- Postgresql
- Django

###Setting up###

To run __Limber__ locally follow the following steps:

1 . Clone the repo and navigate to the project directory
```shell
$ git clone https://github.com/andela/limber.git && cd $_
```


2 . Create a `virtual-env`
```shell
$ virtualenv <env-name>
```


3 . Activate the `virtual-env`
```shell
$ source <env-name>/bin/activate
```


4 . With the `virtual-env` activated, install the project dependencies
```shell
(<env-name>)$ pip install -r requirements.txt
```


5 . If all dependencies install successfully, run the project
```shell
(<env-name>)$ python manage.py runserver
```  

####Running tests####

To run the project tests
```shell
(<env-name>)$ python manage.py test
```
