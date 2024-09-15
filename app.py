from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Welcome to the Car Rental Service!'

# Define the Car model
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_model = db.Column(db.String(80), nullable=False)
    car_type = db.Column(db.String(80), nullable=False)
    registration_number = db.Column(db.String(80), unique=True, nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=False)
    rental_price_per_day = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(20), nullable=False)

# Route to get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify([{
        'id': car.id,
        'car_model': car.car_model,
        'car_type': car.car_type,
        'registration_number': car.registration_number,
        'seating_capacity': car.seating_capacity,
        'rental_price_per_day': car.rental_price_per_day,
        'color': car.color
    } for car in cars])

# Route to add a new car
@app.route('/cars', methods=['POST'])
def add_car():
    data = request.get_json()
    new_car = Car(
        car_model=data['car_model'],
        car_type=data['car_type'],

        registration_number=data['registration_number'],
        seating_capacity=data['seating_capacity'],
        rental_price_per_day=data['rental_price_per_day'],
        color=data['color']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'Car added!'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
