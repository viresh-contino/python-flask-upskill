from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import exc

import os


## Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database Init 
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

class Car(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    colour = db.Column(db.String(20))

    def __init__(self, name, description, price, colour):
        self.name = name 
        self.description = description
        self.price = price 
        self.colour = colour

# @app.route('/', methods=['GET'])
# def get():
#     return jsonify({ 'msg': 'Hello - this is a test get'})

# Car Schema 
class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'colour')

## Init Car Schema 
car_schema = CarSchema()
cars_schema = CarSchema()

# Create a car
@app.route('/car', methods=['POST'])
def add_car():
    name = request.get_json(force=True)['name']
    description = request.get_json(force=True)['description']
    price = request.get_json(force=True)['price']
    colour = request.get_json(force=True)['colour']  

    new_car = Car(name, description, price, colour) 

    try:
        db.session.add(new_car)
        db.session.commit()
        return car_schema.jsonify(new_car)
    except exc.IntegrityError:
        return "Integrity error observerd with entry"

    

# Get all cars
@app.route('/car', methods=['GET'])
def get_all_cars():
    all_cars = Car.query.all()
    result = cars_schema.dump(all_cars,many=True)
    return jsonify(result)

# Get single car
@app.route('/car/<id>', methods=['GET'])
def get_car(id):
    car = Car.query.get(id)
    return car_schema.jsonify(car)


# Update a car
@app.route('/car/<id>', methods=['PUT'])
def update_car(id):
    car = Car.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    colour = request.json['colour']  

    car.name = name 
    car.description = description
    car.price = price 
    car.colour = colour 


    db.session.commit()

    return car_schema.jsonify(car)

# Delete single car
@app.route('/car/<id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    return car_schema.jsonify(car)



if __name__ == '__main__': 
    app.run(debug=True)