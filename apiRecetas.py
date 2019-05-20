from flask import Flask, jsonify, request, make_response, abort
import jwt
import datetime
import os
import psycopg2
from functools import wraps
from cryptography.fernet import Fernet
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = "Secret Key"
llave_cifra = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def toJSON(lista, nombreElemento): #Crea una variable en formato json de una lista, el nombre del elemento es el nombre que se le da en una vatiable
	datos= []

	for url in lista:
		temp = {nombreElemento: url}
		datos.append(temp)

	return datos

def token_required(f): #Comprueba que el token sea válido
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')

		if not token:
			return abort(401)

		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return abort(401)


		return f(*args, **kwargs)
	return decorated

@app.route('/get_recetas', methods=['GET']) #/get_recetas?token=blalblasadfa
@token_required
def getRecetas():
	recetas = ["h","o","l","a","m","u","n","d","o",",","b","u","e","n","a","s",",","s","u","s","a","n","i","t","a","!","!"]
	recetasJSON = {"Nombres" : recetas}
	return jsonify(recetasJSON)

@app.route('/buscar_recetas', methods=['GET']) #/buscar_recetas?cBusqueda=Nombre&strBusqueda=Pollo&token=blalblasadfa
@token_required
def buscarRecetas():

	recetas = ["h","o","l","a","m","u","n","d","o",",","b","u","e","n","a","s",",","s","u","s","a","n","i","t","a","!","!"]
	recetasJSON = {"Nombres" : recetas}
	return jsonify(recetasJSON)


@app.route('/show_receta', methods=['GET']) #/show_receta?nombreReceta=Hola&token=blalblasadfa
@token_required
def showReceta():
	receta = ["Nombre","Tipo",["ing1","ing2","ing3"],["url1","url2"]]

	recetaJSON = {}
	recetaJSON['Nombre'] = receta[0]
	recetaJSON['Tipo'] = receta[1]
	recetaJSON["Ingredientes"] = receta[2]
	recetaJSON["Imagenes"] = receta[3]

	return jsonify(recetaJSON)

@app.route('/create_receta', methods=['POST']) #/create_receta, no está listo
@token_required
def createReceta():
	return jsonify({'mesage' : 'Receta a crear con Token'})


def auth_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		correo = request.args.get('correo')
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM CUENTAS WHERE CUENTAS.correo = '"+correo+"'") #Pide a la base de datos el usuario que comparta el correo
		res = cursor.fetchone()
		print(res)
		if (res == []):
			return abort("El usuario o la contraseña son incorrectos")
		else: 
			cipher_suite = Fernet(llave_cifra)
			contrasena = res[1].encode()
			contrasena = cipher_suite.decrypt(contrasena) #Descifrar
			contrasena = contrasena.decode()

			if (contrasena != request.args.get('contrasena')):
				return abort("El usuario o la contraseña son incorrectos")
		cursor.close()
		return f(*args, **kwargs)
	return decorated

@app.route('/login', methods=['GET']) #/login?correo=correofalso@gmail.com&contrasena=contrasena
@auth_required
def login():
	correo = 	request.args.get('correo')
	token = jwt.encode({'user': correo, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
	return jsonify({'token': token.decode('UTF-8')})

@app.route('/singUp',methods=['POST']) # /singUp?correo=correofalso@gmail.com&contrasena=helado123
def singUp():
	correo = request.args.get('correo')
	contrasena = request.args.get('contrasena')

	
	try:

		cipher_suite = Fernet(llave_cifra)
		contrasena = cipher_suite.encrypt(contrasena.encode())   #Para cifrar 
		contrasena = contrasena.decode()# convertir el binario a texto

		cursor = conn.cursor()
		cursor.execute("INSERT INTO cuentas VALUES (%s, %s)",(correo,contrasena)) #Intenta agregar el nuevo usuario a la base de datos
		conn.commit()
		cursor.close()
		return jsonify({'message': 'El usuario ha sido registrado'})
	except: #Falla si el correo ya existe en la base de datos
		return jsonify({'message': 'El usuario ya está registrado'})


if __name__ == '__main__':
    app.run()