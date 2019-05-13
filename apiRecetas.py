from flask import Flask, jsonify, request, make_response
import jwt
import datetime
import os
import psycopg2
from functools import wraps


DATABASE_URL = os.environ['postgres://jindmszffjwbze:7fbd8d5436109918c3b9d3af00bbd0e7b6ce10dee69c736d79e393405ebd9e12@ec2-54-235-208-103.compute-1.amazonaws.com:5432/d9agm875675pud']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)
app.config['SECRET_KEY'] = "Prueba12345"

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')

		if not token:
			return jsonify({'mesage' : 'No hay Token'}),403

		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return jsonify({'mesage' : 'Token invalido'}),403


		return f(*args, **kwargs)
	return decorated

@app.route('/get_recetas')
@token_required
def getRecetas():
	return jsonify({'mesage' : 'Recetas detras de Token'})

@app.route('/show_receta')
@token_required
def showReceta():
	return jsonify({'mesage' : 'Contenido de receta con Token'})

@app.route('/create_receta')
@token_required
def createReceta():
	return jsonify({'mesage' : 'Receta a crear con Token'})


@app.route('/login')
def login():
	auth= request.authorization

	if auth and auth.password == "password":
		token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])

		return jsonify({'token': token.decode('UTF-8')})
	return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Requerido"'})

if __name__ == '__main__':
    app.run()