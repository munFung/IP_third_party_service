from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Third Party!'

# Define the Car model
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_model = db.Column(db.String(80), nullable=False)
    car_type = db.Column(db.String(80), nullable=False)
    registration_number = db.Column(db.String(80), unique=True, nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=False)
    rental_price_per_day = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(20), nullable=False)

# Define the CarRental model with car_id and room_booking_id attributes
class CarRental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)  # Foreign key to Car table
    room_booking_id = db.Column(db.Integer, nullable=False)  # Foreign key or Integer

    car = db.relationship('Car', backref=db.backref('car_rentals', lazy=True))

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

# Route to get all car rentals
@app.route('/car_rentals', methods=['GET'])
def get_car_rentals():
    car_rentals = CarRental.query.all()
    return jsonify([{
        'id': car_rental.id,
        'car_id': car_rental.car_id,
        'room_booking_id': car_rental.room_booking_id,
        'car_model': car_rental.car.car_model,
    } for car_rental in car_rentals])

# Route to add a new car rental
@app.route('/car_rentals', methods=['POST'])
def add_car_rental():
    data = request.get_json()
    new_car_rental = CarRental(
        car_id=data['car_id'],
        room_booking_id=data['room_booking_id']
    )
    db.session.add(new_car_rental)
    db.session.commit()
    return jsonify({'message': 'Car rental added!'}), 201


# Route to get car rental price by car_id
@app.route('/car_price/<int:car_id>', methods=['GET'])
def get_car_price(car_id):
    car = Car.query.get(car_id)
    if car:
        return jsonify({
            'car_id': car.id,
            'car_model': car.car_model,
            'rental_price_per_day': car.rental_price_per_day
        }), 200
    else:
        return jsonify({'message': 'Car not found'}), 404

# Catering Services
# Define the CateringPackage model
class CateringPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(255), nullable=False)
    package_description = db.Column(db.String(255), nullable=False)
    cuisine_type = db.Column(db.String(100), nullable=False)
    price_per_pax = db.Column(db.Float, nullable=False)


# Example Route to Get All Catering Packages
@app.route('/catering_packages', methods=['GET'])
def get_catering_packages():
    packages = CateringPackage.query.all()
    return jsonify([{
        'id': package.id,
        'package_name': package.package_name,
        'package_description': package.package_description,
        'cuisine_type': package.cuisine_type,
        'price_per_pax': package.price_per_pax
    } for package in packages])



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
