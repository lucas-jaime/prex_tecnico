from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import platform
import psutil
import socket
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ServerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), nullable=False)
    processor = db.Column(db.String(100))
    os_name = db.Column(db.String(100))
    os_version = db.Column(db.String(100))
    users = db.Column(db.String(255))
    date = db.Column(db.String(10))



@app.route('/collect_data', methods=['POST'])
def collect_data():
    data = request.get_json()
    
    ip_address = data.get('ip_address')
    processor = data.get('processor')
    os_name = data.get('os_name')
    os_version = data.get('os_version')
    users = data.get('users')
    date = data.get('date')
    
    # Guardar la información en la base de datos
    new_server_info = ServerInfo(
        ip_address=ip_address,
        processor=processor,
        os_name=os_name,
        os_version=os_version,
        users=users,
        date=date
    )
    
    db.session.add(new_server_info)
    db.session.commit()
    
    return jsonify({"message": "Data collected successfully!"}), 201

@app.route('/get_server_info/<ip>', methods=['GET'])
def get_server_info(ip):
    server = ServerInfo.query.filter_by(ip_address=ip).first()
    
    if server:
        return jsonify({
            "ip": server.ip_address,
            "processor": server.processor,
            "os_name": server.os_name,
            "os_version": server.os_version,
            "users": server.users,
            "date": server.date
        }), 200
    else:
        return jsonify({"error": "Server not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=5000)
