from flask import Flask, jsonify, request, make_response
import jwt
import datetime
import os
import psycopg2
from functools import wraps
from cryptography.fernet import Fernet


app = Flask(__name__)
app.config['SECRET_KEY'] = "Secret Key"
llave_cifra = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def token_required(f):
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

@app.route('/get_recetas',METHODS=['GET'])
@token_required
def getRecetas():
	return jsonify({'mesage' : 'Recetas detras de Token'})

@app.route('/show_receta',METHODS=['GET'])
@token_required
def showReceta():
	return jsonify({'mesage' : 'Contenido de receta con Token'})

@app.route('/create_receta',METHODS=['POST']) ##asosaoidnss.heroku
@token_required
def createReceta():
	return jsonify({'mesage' : 'Receta a crear con Token'})


def auth_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		cursor = conn.cursor()
		cursor.callproc("BuscarUsuario",[auth.username,])
		res = cursor.fetchone()
		if (res == []):
			return abort("El usuario o la contraseña son incorrectos")

		else: 
			cipher_suite = Fernet(key)
			contrsena = (cipher_suite.decrypt(res[1][2])) #Descifrar
			if (contrsena != auth.password):
				return abort("El usuario o la contraseña son incorrectos")

@app.route('/login', METHODS=['GET'])
@auth_required
def login():
	token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
	return jsonify({'token': token.decode('UTF-8')})

@app.route('singUp',METHODS=['POST'])
	def singUp():
		correo = request.args.get('correo')
		contrasena = request.args.get('contrasena')

		cursor = conn.cursor()
		cursor.callproc("GetUsuarios",[,])
		res = cursor.fetchall()

		for tupla in res
			if (tupla[1] == correo):
				return abort("El correo ya está asociado a otra cuenta")


	contrasena = ' '.join(format(ord(x), 'b') for x in contrasena)
	cipher_suite = Fernet(key)
	ciphered_text = cipher_suite.encrypt(contrasena)   #Para cifrar 

	cursor.callproc("InsertarUsuarios",[correo,contrasena,])
	return jsonify{'message': 'El usuario ha sido registrado'}


if __name__ == '__main__':
    app.run()