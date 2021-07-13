
import pandas as pd  
import os
import psycopg2 as ps
import requests
from flask.json import jsonify
from pandas.io.json import json_normalize
import json
from shapely.geometry import Point, MultiPoint
import geopandas as gpd
import time

# Este Script consume la api que proporciona la CDMX para consultar la posicion por hora
# de cada vehiculo del metrobus y carga los datos a una base de datos postgresql.
# Ademas de cargar los datos realiza el calculo para saber en que alcaldia se encuentra el punto y
#igual forma se carga a la base

while True:

	#Consumo de api y transformacion de datos
	r = requests.get('https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=prueba_fetchdata_metrobus&rows=300')
	data = r.json()
	cord = pd.json_normalize(data['records'])
	points = cord[['fields.position_longitude','fields.position_latitude']]
	points= [tuple(x) for x in points.values]
	size = len(points)
	points =  MultiPoint(points)

	# Configuracion de credenciales 

	with open("./config.json") as file:
		conf = json.load(file)
		
	conexion = ps.connect(host=conf['Host'],
						database=conf['database'],
						user=conf['user'],
						port=conf['port'], 
						password=conf['password'])



	cur = conexion.cursor()
	sqlquery = 'SELECT poligono, name FROM alcaldias';
	region = gpd.read_postgis(sqlquery, conexion, geom_col= 'poligono')


	#Calculo de punto en poligono y carga de base de datos

	for ind, row2 in cord.iterrows() :
		for i,row in region.iterrows():
			if row['poligono'].contains(points[ind]):
				sqlquery = "INSERT INTO mb_ubicacion (nom_alcaldia,id_mb,date_time,longitud,latitud) VALUES (%s,%s,%s,%s,%s);"
				parametros = (row['name'],
						row2['fields.vehicle_id'],
						row2['fields.date_updated'],
					  	row2['fields.position_longitude'],
					  	row2['fields.position_latitude']
					  	
					)
				
				cur = conexion.cursor()
				cur.execute(sqlquery,parametros)
				break
		



	cur = conexion.cursor()
	sqlquery = "SELECT COUNT(*) FROM mb_ubicacion;"
	cur.execute(sqlquery)
	count = cur.fetchall()


	# Limite de numero de numero de registros en la base

	if count[0][0] > 5000:
		sqlquery = "DELETE FROM mb_ubicacion WHERE indice = (SELECT MIN(indice) FROM mb_ubicacion);"
		cur.execute(sqlquery,parametros)

		
	conexion.commit()
	cur.close()

	time.sleep(3600)
