import json
import model
import hashlib
import datetime
from flask import abort

#Converte os dados recebidos para o formato json
#caso os mesmos nao estejam no formato correto
#retorna um erro
def convert_to_json(data):
	
	try:
		data = json.loads(data)
	except Exception as e:
		abort(400, description = "Formato dos dados invalido.")
	
	return data

#Gera um hash de acordo com os dados recebidos da requisicao
def generate_request_hash(request):
	
	req_str = str(request).encode('utf-8')
	req_hash = hashlib.md5(req_str)
	req_hash = req_hash.hexdigest()

	return req_hash 

#calcula a diferença entre duas datas
#retornando o valor em minutos
def calculate_date_diff(date1, date2):

	date_diff = date1 - date2
	diff_in_sec = date_diff.total_seconds()
	diff_in_min = diff_in_sec / 60

	return diff_in_min

#processa a requisicao recebida criando o hash da mesma.
#caso nao exista nenhuma outra requisicao 
# com o mesmo body na base de dados, persiste a requisicao
#caso exista uma requisicao com o mesmo body
#mas ela tenha sido recebida num intervalo maior que
#10 minutos em relação a que esta sendo processada, persiste a mesma
#caso contrario, retorna um erro.
def process_request(request, date_time):
	
	req_hash = generate_request_hash(request)
	
	request_old = model.find_request(req_hash)

	max_minutes_diff = 10

	if request_old == None:
		model.persist_request(request, req_hash)
	else:

		dt_time_old = request_old['creation_date_time']

		minutes_diff = calculate_date_diff(datetime.datetime.now(), dt_time_old)
		
		if minutes_diff > max_minutes_diff:
			model.persist_request(request, req_hash)
		else:
			abort(403, description = "Corpo da requisicao duplicada no intervalo de "+str(max_minutes_diff)+" minutos.")

	return {'success': 'Requisicao processada com sucesso.'}

#Processa os produtos contidos nas requisicoes recebidas
#atualizando e criando novos produtos
def process_products():
	pass