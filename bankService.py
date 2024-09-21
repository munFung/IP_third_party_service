from flask import Flask, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bankService.db'
db = SQLAlchemy(app)

key = Fernet.generate_key()
print(key.decode())  # Store this key safely
cipher = Fernet(key)

@app.route('/')
def index():
    return 'Bank Service Third Party!'

# Serve the 'add.html' file
@app.route('/add_bank_account', methods=['GET'])
def add_bank_account_form():
    return render_template('add.html')  # Render the add.html page from templates folder

@app.route('/get_key', methods=['GET'])
def get_key():
    # This should be secured with some form of authentication
    return jsonify({'key': key.decode()}), 200


# Define the BankAccount model
class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_holder = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    bank = db.Column(db.String(100), nullable=False)  # Added bank field
    account_pin = db.Column(db.String(6), nullable=False)  # Added account_pin field

    @staticmethod
    def encrypt_pin(pin):
        return cipher.encrypt(pin.encode()).decode()

    @staticmethod
    def decrypt_pin(encrypted_pin):
        return cipher.decrypt(encrypted_pin.encode()).decode()

# Route to get all bank accounts
@app.route('/bank_accounts', methods=['GET'])
def get_bank_accounts():
    accounts = BankAccount.query.all()
    return jsonify([{
        'id': account.id,
        'account_number': account.account_number,
        'account_holder': account.account_holder,
        'balance': account.balance,
        'bank': account.bank,
        'account_pin': BankAccount.decrypt_pin(account.account_pin)  # Decrypt the pin for display
    } for account in accounts])

# Route to add a bank account
@app.route('/bank_accounts', methods=['POST'])
def add_bank_account():
    data = request.get_json()
    new_account = BankAccount(
        account_number=data['account_number'],
        account_holder=data['account_holder'],
        balance=data['balance'],
        bank=data['bank'],
        account_pin=BankAccount.encrypt_pin(data['account_pin'])
    )
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Bank account added!'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5002, debug=True)
