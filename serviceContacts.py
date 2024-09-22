from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# REMEMBER TO CHANGE THE DB NAME
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_contacts.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Service Contacts Third Party!'

# Define the ServiceContact model
class ServiceContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False) 

# Route to get all service contacts
@app.route('/service_contacts', methods=['GET'])
def get_service_contacts():
    contacts = ServiceContact.query.all()
    return jsonify([{
        'id': contact.id,
        'name': contact.name,
        'phone': contact.phone,
        'email': contact.email,
        'role': contact.role,
        'company_name': contact.company_name,
        'status': contact.status, 
    } for contact in contacts])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5004, debug=True)
