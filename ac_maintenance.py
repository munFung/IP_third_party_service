from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coldice_company.db'
db = SQLAlchemy(app)

# Define HistoryOfService model
class HistoryOfService(db.Model):
    __tablename__ = 'history_of_service'

    id = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(255), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    maintenance_date = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __init__(self, hotel_name, room_number, maintenance_date, cost):
        self.hotel_name = hotel_name
        self.room_number = room_number
        self.maintenance_date = maintenance_date
        self.cost = cost

# Define RequestOfMaintenance model
class RequestOfMaintenance(db.Model):
    __tablename__ = 'request_of_maintenance'

    id = db.Column(db.Integer, primary_key=True)
    hotel_name = db.Column(db.String(255), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    rooms = db.Column(db.String(255), nullable=False)  # Store room numbers as a comma-separated string

    def __init__(self, hotel_name, request_date, rooms):
        self.hotel_name = hotel_name
        self.request_date = request_date
        self.rooms = rooms

# Route to get service history
@app.route('/service_history', methods=['GET'])
def get_service_history():
    service_history = HistoryOfService.query.all()
    return jsonify([{
        'id': record.id,
        'hotel_name': record.hotel_name,
        'room_number': record.room_number,
        'maintenance_date': record.maintenance_date.isoformat(),  # Format the date
        'cost': record.cost
    } for record in service_history])



# Initialize the database tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(host='127.0.0.1', port=5003, debug=True)
