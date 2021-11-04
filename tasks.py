from celery import Celery
from time import sleep
from app import add_car
from sqlalchemy import exc
import requests

app = Celery('tasks', broker='amqp://guest:guest@localhost:5672/', backend='db+sqlite:///db.sqlite3')

@app.task
def add_car(car_name):
    sleep(1)
    # response = requests.post('https://httpbin.org/post', data = {'key':'value'})

    r = requests.post('http://127.0.0.1:5000/car', json = { "name": car_name, 
                                                            "description": "added via celery task", 
                                                            "price": 0,
                                                            "colour": "empty" } 
                        
                                                     )

    return r.text
