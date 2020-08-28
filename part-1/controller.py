from flask import Flask, request, jsonify
import util
import model
import datetime

app = Flask(__name__)

@app.route('/v1/products/', methods=['POST'])
def index():
	
	data = request.get_data()

	data = util.convert_to_json(data)

	response = util.process_request(data, datetime.datetime.now())

	return response

@app.errorhandler(500)
@app.errorhandler(400)
@app.errorhandler(403)
def handle_error(e):
	return jsonify(error=str(e))

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5098)