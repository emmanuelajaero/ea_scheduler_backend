from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import sys

from initial_values import initial_employees, initial_services, initial_holidays
from models import load_services, load_employees, load_holidays, initialize, get_user, get_users, get_services, create_workorder

# functions that will be executed from command line
def cmd_map(command):
	if command == "--ea-load-services":
		load_services(initial_services)
	if command == "--ea-load-employees":
		load_employees(initial_employees)
	if command == "--ea-load-holidays":
		load_holidays(initial_holidays)
	if command == "--ea-initialize":
		initialize()

#extract the commands from the command line
cmd_params = sys.argv[1:]

#run the commands from command line
for command in cmd_params:
	cmd_map(command)


app = Flask(__name__)
CORS(app)

@app.route("/get/user/by/id", methods=["GET", "POST"])
def get_user_by_id():
	if request.is_json:
		req = request.get_json()
		user = get_user(req)

		response_body = {"status": "success","user": user} if user else {"status": "failed", "message": "Not a user"}

		res = make_response(jsonify(response_body), 200)
		return res
	else:
		return make_response(jsonify({"status":"failed", "message": "Request body not formated properly"}), 400)


@app.route("/get/users/by/role", methods=["GET", "POST"])
def get_user_by_role():
	if request.is_json:
		req = request.get_json()
		users = get_users(req)

		response_body = {"status": "success","users": users} if users else {"status": "failed", "message": "No user with the role"}

		res = make_response(jsonify(response_body), 200)
		return res
	else:
		return make_response(jsonify({"status":"failed", "message": "Request body not formated properly"}), 400)


@app.route("/get/services", methods=["GET", "POST"])
def fetch_services():
	services = get_services()

	response_body = {"status": "success","services": services} if services else {"status": "failed", "message": "No services in db"}

	res = make_response(jsonify(response_body), 200)
	return res




@app.route("/add/workorder", methods=["POST"])
def add_workorder():
	if request.is_json and request.method == "POST":
		req = request.get_json()
		workorder = create_workorder(req)

		print("workorder : ", workorder)
		response_body = {"status": "success" if workorder["inserted"] else "failed","message": workorder["message"]} if workorder else {"status": "failed", "message": "No plese try again"}

		res = make_response(jsonify(response_body), 200)
		return res
	else:
		return make_response(jsonify({"status":"failed", "message": "Request body not formated properly or the method is not POST"}), 400)



if __name__=='__main__':
    app.run(debug=True)

