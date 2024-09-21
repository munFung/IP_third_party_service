from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# REMEMBER TO CHANGE THE DB NAME
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zhengyao.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return '#### Third Party!'



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5004, debug=True)
