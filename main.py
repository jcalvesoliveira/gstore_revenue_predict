# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:08:34 2018

@author: JULIO
"""
from flask import Flask, request, jsonify, Response
from functools import wraps
import json
from sklearn.ensemble import GradientBoostingRegressor
import pickle


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


clf = pickle.load(open('gb_model_reduced.pkl','rb'))



#Creating a simple get end-point only for test purpose
@app.route('/')
@requires_auth
def hello():
	"""Basic index to verify app is serving."""
	return 'Hello World!'





#This end-point is able to receive ajson and make a predictiont
@app.route('/gb_model', methods=['POST'])
@requires_auth
def post():
	print(request.headers)
	print(request.data)
	items=request.get_json(force=True)
	print(items)
	
	#Saving the id's of the request into a variable
	if type(items) == str:
		text = json.loads(items.replace('\\',''))['Text']
	elif type(items) == dict:
		text = items['Text']
		id_text = items['Id']

	

	if not len(text) == len(id_text):
		return	jsonify({"Result":"Lenghts of arrays does not match"}), 201

		text_std = TextClean(text)
		print(text_std)
		features = tfidf.transform(text_std)
		predicted = clf.predict(features)

		
			
	#Return the response for each Id in a json format     
	return jsonify([{"Id": str(id_text), "Result": bool(predicted[i])} for i,id_text in enumerate(id_text)]), 201

if __name__ == '__main__':
	# This is used when running locally. Gunicorn is used to run the
	# application on Google App Engine. See entrypoint in app.yaml.
	app.run(host='127.0.0.1', port=8080, debug=True)