import platform
import psutil
import socket
import requests
import datetime
import os

# Recolectar información del sistema
def get_system_info():
    ip_address = socket.gethostbyname(socket.gethostname())  # IP del servidor
    processor = platform.processor()
    os_name = platform.system()
    os_version = platform.version()

    # Obtener los usuarios conectados
    users = []
    for user in psutil.users():
        users.append(user.name)
    users = ', '.join(users)
    
    # Fecha actual en formato AAAA-MM-DD
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    return {
        "ip_address": ip_address,
        "processor": processor,
        "os_name": os_name,
        "os_version": os_version,
        "users": users,
        "date": date
    }

# Enviar datos a la API
def send_data_to_api(data):
    url = "http://3.137.162.127:5000/collect_data"
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print("Data sent successfully!")
    else:
        print("Failed to send data")

# Función principal
if __name__ == '__main__':
    system_info = get_system_info()
    send_data_to_api(system_info)
