from faker import Faker
import itertools
from flask import Flask, request # type: ignore
from sqlalchemy import create_engine # type: ignore
import json
import sys
import logging
import os

app =  Flask(__name__)
fake = Faker()
logger = logging.getLogger(__name__)

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Configuración básica del logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=os.path.join(log_dir, 'app.log'),
                    filemode='a')

@app.route('/random')
def random_data():
	insert_queries = []
	campos = ['job', 'company', 'ssn', 'residence', 'blood_group']
	profiles = [{campo: fake.profile()[campo] for campo in campos} for _ in range(13)]
	logger.info(f'CREANDO DATA {profiles}')
	for profile in profiles:
		sql =""
		values = (str(list(profile.values())).replace("\\","")[1:-1])
		sql =f""" INSERT INTO profile (job, 
									 company, ssn, 
									 residence,
									 blood_group)
			   VALUES ({values});""".replace("\n","")
		insert_queries.append(sql)
		logger.info(f'EJECUTANDO SQL: {sql}')
	return insert_queries

@app.route('/executeDB')
def execute_queries(list_queries_string=[], querie_type=''):
	db_name = 'rainbow_database'
	db_user = 'unicorn_user'
	db_pass = 'magical_password'
	db_host = 'database-service-hotel' # este es el servicio database declarado en el docker-compose
	db_port = '5432'
	# conexion a la base de datos POSTGRESQL
	try:
		db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
		logging.info(f"DB INFO: {db_string}")
		db = create_engine(db_string)
		logger.info('VOY EXECUTE QUERYS*********************************************')
		if querie_type == 'INSERT':
			for querie in list_queries_string:
				db.execute(querie).rowcount
		if querie_type == 'SELECT':
			all_data = []
			for querie in list_queries_string:
				logger.info('VOY POR EXECUTE SELECT*********************************************')
				result = db.execute(querie) 
				data_profiles = [dict(row) for row in result.fetchall()]
				all_data.extend(data_profiles)
				logger.info(f'TERMINA EXECUTE SELECT, VA A RETORNAR********************************************* {data_profiles}')
			return all_data
		if querie_type == 'DELETE':
			for querie in list_queries_string:
				data_profiles = db.execute(querie)

		##EJECUCIÓN RESERVATION

		if querie_type == 'INSERT_RESERVATION':
			for querie in list_queries_string:
				db.execute(querie).rowcount
		if querie_type == 'SELECT_RESERVATION':
			all_data = []
			for querie in list_queries_string:
				logger.info('VOY POR EXECUTE SELECT RESERVATION*********************************************')
				result = db.execute(querie)
				data_profiles = [dict(row) for row in result.fetchall()]
				all_data.extend(data_profiles)
				logger.info(f'TERMINA EXECUTE SELECT, VA A RETORNAR********************************************* {data_profiles}')
			return all_data
		if querie_type == 'DELETE_RESERVATION':
			for querie in list_queries_string:
				data_profiles = db.execute(querie)
		return {"message":"proceso correcto"}
	except Exception as e:
		print("error en conexion con la base de datos", e)
		return {"status":f"Error en la conexión con la base de datos: {e}"}


@app.route('/crear_registros')
def create_profiles():
	try:
		logger.info('VOY POR CREAR REGISTROS*********************************************')
		execute_queries(random_data(),"INSERT")
		logger.info('VOY A TERMINAR CREAR REGISTROS REGISTROS*********************************************')
		return {"message":"proceso realizado correctamente"}
	except Exception:
		return {"message":"error en proceso de creacion de datos en faker-service"}

@app.route('/obtener_registros')
def get_profiles():
	querie_data= 'SELECT * FROM profile;'
	try:
		logger.info('VOY A EJECUTAR OBTENER REGISTROS*********************************************')
		data_profiles = execute_queries([querie_data], "SELECT")
		logger.info(f'EJECUTE OBTENER REGISTROS, VOY A RETORNARRR********************************************* {data_profiles}')
		return json.dumps(data_profiles)
	except Exception as e:
		return {f"message":f"Error en la conexión con la base de datos: {e}"}

@app.route('/borrar_registros')
def delete_profiles():
	querie_data= 'DELETE FROM profile;'
	try:
		data_profiles =  execute_queries([querie_data],"DELETE")
		return json.dumps(data_profiles)
	except Exception:
		return {"message":"error en eliminacion de datos en servicio faker-service"}
	
################################################################# GESTION DATOS RESERVATION

@app.route('/crear_registros_reservation')
def create_reservation():
	##FORMATO REQUEST: GET /crear_registros_reservation?start_date=2024-01-01&end_date=2024-01-31&user=usuario_ejemplo
	start_date = request.args.get('start_date')
	end_date = request.args.get('end_date')
	user = request.args.get('user')

	try:
		logger.info(f'VOY POR CREAR REGISTROS DATOS: {start_date}{end_date}{user}')
		insert_queries=[]
		sql =""
		sql =f""" INSERT INTO reservation(
    									id,
    									checkin_date,
    									checkout_date,
										idprofile)
				VALUES ((SELECT MAX(ID)+1 FROM reservation) 
				,'{start_date}'
				,'{end_date}'
				,{user})
			   """.replace("\n","")
		insert_queries.append(sql)
		logger.info(f'EJECUTANDO SQL: {sql}')
		execute_queries(insert_queries,"INSERT_RESERVATION")
		logger.info('VOY A TERMINAR CREAR REGISTROS REGISTROS*********************************************')
		return {"message":"proceso realizado correctamente"}
	except Exception:
		return {"message":"error en proceso de creacion de datos en faker-service"}

@app.route('/obtener_registros_reservation')
def get_reservation():
	querie_data= f"""SELECT 
    					ID,
    					TO_CHAR(checkin_date, 'YYYY-MM-DD') AS checkin_date,
    					TO_CHAR(checkout_date, 'YYYY-MM-DD') AS checkout_date,
    					idprofile
					FROM reservation;"""
	try:
		logger.info('VOY A EJECUTAR OBTENER REGISTROS*********************************************')
		data_reservation = execute_queries([querie_data], "SELECT_RESERVATION")
		logger.info(f'EJECUTE OBTENER REGISTROS, VOY A RETORNARRR********************************************* {data_reservation}')
		return json.dumps(data_reservation)
	except Exception as e:
		return {f"message":f"Error en la conexión con la base de datos: {e}"}

@app.route('/borrar_registros_reservation')
def delete_reservation():
	##FORMATO REQUEST: GET /borrar_registros_reservation?id_reservation=2
	id_reservation = request.args.get('id_reservation')
	querie_data= f'DELETE FROM reservation WHERE id = {id_reservation}'
	logger.info(f"VA A EJECUTAR EL QUERY {querie_data}")
	try:
		data_profiles =  execute_queries([querie_data],"DELETE")
		return json.dumps(data_profiles)
	except Exception:
		return {"message":"error en eliminacion de datos en servicio faker-service"}

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)

