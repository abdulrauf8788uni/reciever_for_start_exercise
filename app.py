from flask import Flask, jsonify, request
import os
import json
from dotenv import load_dotenv

from exercise_code.manager import MachineManager

app = Flask(__name__)
load_dotenv()

@app.route('/', methods=['GET'])
def index():
	return jsonify({"message": "Hello World"}), 200

@app.route('/start/', methods=['POST'])
def start():
	context = json.loads(request.data)
	print(context)
	if context.get("server_key") != os.environ.get("SERVER_KEY"):
		return jsonify({"detail": "Authentication credentials were not provided."}), 401 # HTTP 401 Unauthorized

	manager = MachineManager()
	status = manager.start_exercise(context)
	if status:
		return jsonify({"status": "1" ,'detail': 'Exercise Started Successfully.'}), 200 # HTTP 200 OK
	return jsonify({"status": "0" ,'detail': "Exercise machine not available"}), 200

if __name__ == '__main__':
	app.run()