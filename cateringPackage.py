from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catering_service.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Catering Service Third Party!'


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
    app.run(host='127.0.0.1', port=5001, debug=True)
