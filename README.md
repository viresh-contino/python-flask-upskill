# python-flask-upskill
Python Flask Upskilling Project  

## Description
The aim of this project is to introduce you to the following Python packages:
- sql alchemym( db orm)
- marshmallow - db serialization
- flask - api server
- celery 


### Versions
```bash
$ python --version
Python 3.9.2 
```

### Commands 
```bash
$ pip3 install pipenv
$ pipenv install flask flask-sqlalchemy flask-marshmallow flask-sqlalchemy marshmallow-sqlalchemy celery
# this will use the pipenv shell with installed pip packages
$ pipenv shell 
# create the app.py
$ touch app.py
# start flask app.py
$python app.py
```

### Postman
Use postman to invoke the flask api to do the following:
- add car
- get all cars
- update car
- delete car 


### Rabit MQ and Celery for task execution

![vscode - celery in operation](/notes/celery-vscode.png)

#### Terminal 1
Here we are running the  celery service as per tasks.py
```bash
$ celery -A tasks worker --loglevel=info
```
#### Terminal 2
Here we are going to run rabbitmq message queue service via docker-compose
```
$ docker-compose up
```
#### Terminal 3
Here, we are going to execute a python method via celery by running an adhoc python script via the terminal
```bash
(python-flask-upskill) ➜  python-flask-upskill git:(main) ✗ python
Python 3.9.2 (default, Mar 26 2021, 23:22:38) 
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from tasks import reverse
>>> reverse.delay('Viresh')
<AsyncResult: 4d8d741f-6308-4834-b41a-1ec4bc3700d6>
```


### Use sqlite3 for the celery backend
Create the sqlite3 backend storage
```
(python-flask-upskill) ➜  python-flask-upskill git:(main) ✗ sqlite3 db.sqlite3
SQLite version 3.32.3 2020-06-18 14:16:19
Enter ".help" for usage hints.
sqlite> .tables
sqlite> .exit
```
### with the backend, poll the celery task for status and results
```bash
(python-flask-upskill) ➜  python-flask-upskill git:(main) ✗ python
Python 3.9.2 (default, Mar 26 2021, 23:22:38) 
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from tasks import reverse
>>> reverse.delay('this is another celery attempt')
<AsyncResult: 06529276-bcd1-4d79-b375-c8f30eee0114>
>>> res = reverse.delay('this is another celery attempt')
>>> res
<AsyncResult: a22e9803-80eb-4044-878a-7cdc84287279>
>>> res.status
'PENDING'
>>> res.status
'SUCCESS'
>>> res.status
'SUCCESS'
>>> res.get
<bound method AsyncResult.get of <AsyncResult: a22e9803-80eb-4044-878a-7cdc84287279>>
>>> res.get()
'tpmetta yrelec rehtona si siht'
```
### Look in sqlite database tables for the execution results created by Celery
```
(python-flask-upskill) ➜  python-flask-upskill git:(main) ✗ sqlite3 db.sqlite3
SQLite version 3.32.3 2020-06-18 14:16:19
Enter ".help" for usage hints.
sqlite> .tables
celery_taskmeta     celery_tasksetmeta
sqlite> select * from celery_taskmeta ;
1|ead4baed-055c-4ab8-aac5-9a847f023b4c|SUCCESS|��"|2021-11-01 10:27:53.852969|||||||
2|3ac29a55-5d23-4a94-8424-6030ce241ffc|SUCCESS|�� |2021-11-01 10:29:17.693115|||||||
sqlite> .exit
```

### view the Rabbit MQ management web interface exposed on port 15672