from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bankService.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Bank Service Third Party!'


# Define the BankAccount model
class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_holder = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    bank = db.Column(db.String(100), nullable=False)  # Added bank field
    account_pin = db.Column(db.String(6), nullable=False)  # Added account_pin field

# Route to get all bank accounts
@app.route('/bank_accounts', methods=['GET'])
def get_bank_accounts():
    accounts = BankAccount.query.all()
    return jsonify([{
        'id': account.id,
        'account_number': account.account_number,
        'account_holder': account.account_holder,
        'balance': account.balance,
        'bank': account.bank,  # Added bank field
        'account_pin': account.account_pin  # Added account_pin field
    } for account in accounts])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5002, debug=True)
