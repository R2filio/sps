from flask import Flask, render_template, request, Response
import requests
from flask.json import jsonify
import psycopg2 as ps
import json
import pandas as pd 
import geopandas as gpd
from pandas.io.json import json_normalize
from datetime import datetime
from postgis.psycopg import register
from shapely.geometry import Point, MultiPoint
from shapely.geometry.polygon import Polygon
from app import app

# Metodos para cada ruta de la api


# Configuracion de credenciales 
with open("./config.json") as file:
	conf = json.load(file)


conexion = ps.connect(host=conf['Host'],
						database=conf['database'],
						user=conf['user'],
						port=conf['port'], 
						password=conf['password'])

cur = conexion.cursor()


# regresa una lista de la posicion geografica de cada uno de los metrobuses
# asi como la alcaldia donde se encuentran

@app.route('/ubicacion', methods = ['GET'])
def ubicacion():
   
    sqlquery = "SELECT * FROM mb_ubicacion WHERE date_time = (SELECT MAX(date_time) FROM mb_ubicacion);"
    data = pd.read_sql_query(sqlquery, conexion)
    result = {}
    for index, row in data.iterrows():
        result[index] = dict(row)

    return jsonify(result)

# regresa el historial de un dia completo de un metrobus(id_mb)

@app.route('/historial/<int:id_mb>', methods = ['GET'])
def historial(id_mb):


	sqlquery = 'SELECT * FROM mb_ubicacion WHERE id_mb = {}'.format(id_mb);
	data = pd.read_sql_query(sqlquery, conexion)

	result = {}
	for index, row in data.iterrows():
	    result[index] = dict(row)

	return jsonify(result)

# regresa una lista de alcaldias en la ultima hora.

@app.route('/alcaldias', methods = ['GET'])
def alcaldias():
	cur = conexion.cursor()
	sqlquery = 'SELECT poligono, name FROM alcaldias';
	region = gpd.read_postgis(sqlquery, conexion, geom_col= 'poligono')
	
	sqlquery = 'SELECT longitud,latitud FROM mb_ubicacion WHERE date_time = (SELECT MAX(date_time) FROM mb_ubicacion)';
	cur.execute(sqlquery)
	points = cur.fetchall()
	size = len(points)
	points =  MultiPoint(points)
	
	region['Habilitada'] = None

	for i,row in region.iterrows():
		for n in range(size):
			if row['poligono'].contains(points[n]):
				region['Habilitada'].iloc[i] = True
				break
			else:
				region['Habilitada'].iloc[i] = False

	data = region[['name','Habilitada']]
	
	
	result = {}
	
	for index, row in data.iterrows():
	    result[index] = dict(row)

	return jsonify(result)


#regresa el historial de id_mb que estuvieron en una alcaldia determinada(id_alcaldia)
@app.route('/historial/alcaldia/<int:id_alcaldia>', methods = ['GET'])
def u_alcaldias(alcaldia):

	sqlquery = 'SELECT id_mb from mb_ubicacion where nom_alcaldia = (select name from alcaldias where id_alcaldia = {})'.format(id_alcaldia);
	cur.execute(sqlquery)
	data = pd.read_sql_query(sqlquery, conexion)

	data = data.to_dict('dict')

	return jsonify(data)

