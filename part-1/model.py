import pymongo as mdb
from flask import abort
import datetime
import os

#Realiza a conexao com a base de dados
def connect():
	try:
		#connection = mdb.MongoClient("mongodb://localhost:27018/")
		connection = mdb.MongoClient(os.environ['MONGODB_HOSTNAME'], 27017, username='root', password='rootpassword')
	except Exception as e:
		abort(500, description = "Erro ao iniciar conexao com a base de dados. " + str(e))
	
	return connection

#Busca na base de dados por uma requisicao
#com determinado hash
def find_request(req_hash):

	connection = connect()

	database = connection['datalake']

	request_coll = database['request']

	request = request_coll.find_one(
						
						{'req_hash':req_hash}, {'creation_date_time': 1, '_id': 0}, 
						
						sort= [ ("creation_date_time", mdb.DESCENDING) ] 

						)

	connection.close()

	return request


#Persiste a nova requisicao recebida
def persist_request(body, req_hash):

	connection = connect()

	database = connection['datalake']

	request_coll = database['request']
	
	newrequest = { 'body': body, 'req_hash':  req_hash, 'creation_date_time': datetime.datetime.now()}
	
	try:
		request_coll.insert_one(newrequest)
	except Exception as e:
		abort(500, description = "Erro ao persistir a requisicao na base de dados.")

	connection.close()


def createProducts():
	pass