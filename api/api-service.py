from flask import Flask
import requests
import json
import sys
import logging
import os

app =  Flask(__name__)
logger = logging.getLogger(__name__)

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Configuración básica del logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=os.path.join(log_dir, 'app.log'),
                    filemode='a')


@app.route("/")
def home():
	try:
		url = f"http://faker-service:{3000}/obtener_registros"
		res = requests.get(url).json()
		return json.dumps(res)
	except Exception as e:
		print(e, file=sys.stderr) #salida atraves de los logs
		return {"message":"error en consulta de datos"}
   

@app.route("/admin/borrar_registros")
def delete_records():
	url = f"http://faker-service:{3000}/borrar_registros"
	res = requests.get(url).json()
	return json.dumps(res)

@app.route("/admin/crear_registros")
def create_records():
	url = f"http://faker-service:{3000}/crear_registros"
	res = requests.get(url).json()
	return json.dumps(res)

@app.route("/reservation")
def getReservation():
	try:
		url = f"http://faker-service:{3000}/obtener_registros_reservation"
		res = requests.get(url).json()
		logging.info(f"Recibido desde Faker {res}")
		return json.dumps(res)
	except Exception as e:
		print(e, file=sys.stderr) #salida atraves de los logs
		return {"message":"error en consulta de datos"}
   

@app.route("/admin/borrar_registros_reservation")
def deleteReservations():
	url = f"http://faker-service:{3000}/borrar_registros"
	res = requests.get(url).json()
	return json.dumps(res)

@app.route("/admin/crear_registros_reservation")
def create_reservation():
	##FORMATO REQUEST: GET /crear_registros_reservation?start_date=2024-01-01&end_date=2024-01-31&user=usuario_ejemplo
	url = f"http://faker-service:{3000}/crear_registros"
	res = requests.get(url).json()
	return json.dumps(res)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=81, debug=True)