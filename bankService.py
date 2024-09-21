from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import base64
import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bankService.db'
db = SQLAlchemy(app)

# Load the key from the 'key.key' file
with open('key.key', 'rb') as key_file:
    key = key_file.read()

# Use the first 16 bytes of the SHA-256 hash for AES-128
key = hashlib.sha256(key).digest()[:16]

@app.route('/add_bank_account', methods=['GET'])
def add_bank_account_form():
    return render_template('add.html')

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_holder = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    bank = db.Column(db.String(100), nullable=False)
    account_pin = db.Column(db.String(128), nullable=False)

    @staticmethod
    def encrypt_pin(pin):
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        cipher_text = cipher.encrypt(pad(pin.encode(), AES.block_size))
        hmac_signature = hmac.new(key, iv + cipher_text, hashlib.sha256).digest()
        encoded_pin = base64.b64encode(hmac_signature + iv + cipher_text).decode()
        return encoded_pin

    @staticmethod
    def decrypt_pin(encrypted_pin):
        decoded = base64.b64decode(encrypted_pin)
        hmac_signature = decoded[:32]
        iv = decoded[32:48]
        cipher_text = decoded[48:]

        calculated_hmac = hmac.new(key, iv + cipher_text, hashlib.sha256).digest()
        if not hmac.compare_digest(hmac_signature, calculated_hmac):
            raise Exception("Invalid HMAC")

        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(cipher_text), AES.block_size).decode()

@app.route('/bank_accounts', methods=['GET'])
def get_bank_accounts():
    accounts = BankAccount.query.all()
    # Decrypt the account PIN before sending it in the response
    return jsonify([{
        'id': account.id,
        'account_number': account.account_number,
        'account_holder': account.account_holder,
        'balance': account.balance,
        'bank': account.bank,
        'account_pin': BankAccount.decrypt_pin(account.account_pin)  # Decrypt here
    } for account in accounts])

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
