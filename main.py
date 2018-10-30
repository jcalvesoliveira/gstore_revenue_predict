# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:08:34 2018

@author: JULIO
"""
from flask import Flask, request, jsonify, Response
from functools import wraps
import pickle
import pandas as pd


app = Flask(__name__)


#Creating a BasicAuth with username and password
def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""
	return username == 'julio.oliveira' and password == 'E552B551ACD2E7A9'

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

clf = pickle.load(open('model/gb_model_reduced.sav','rb'))



#Creating a simple get end-point only for test purpose
@app.route('/')
@requires_auth
def hello():
	"""Basic index to verify app is serving."""
	return 'Hello World!'





#This end-point is able to receive an json and return the prediction
@app.route('/gb_model', methods=['POST'])
@requires_auth
def post():
	#print(request.headers)
	#print(request.data)
	items=request.get_json(force=True)
	#print(items)
	
	df = pd.read_json(items)

	predicted = clf.predict(df)

		
			
	#Return the response for each Id in a json format     
	#return jsonify([{"Id": str(i), "Result": str(result)} for i,result in enumerate(predicted)]), 201
	return jsonify(prediction=list(predicted)), 201

if __name__ == '__main__':
	# This is used when running locally. Gunicorn is used to run the
	# application on Google App Engine. See entrypoint in app.yaml.
	app.run(host='127.0.0.1', port=8080, debug=True)