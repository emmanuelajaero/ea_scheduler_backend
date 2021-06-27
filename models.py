import mysql.connector
import sys
from schema import tables_definitions
from initial_values import initial_employees, initial_services, initial_holidays
from db_credential import credentials as db
import datetime as prime_date
from datetime import datetime
# print("Initialing...")
# print(sys.argv)



def create_db():
	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"])
	cursor = mydb.cursor()
	cursor.execute(f'CREATE DATABASE {db["database"]}')
	dbs = []
	cursor.execute("SHOW DATABASES")
	for database in cursor:
		dbs.append(database[0])
	cursor.close()
	return dbs


def connect_db():
	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	return mydb.cursor()

def load_services(services):
	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()

	for service in services:
		cursor.execute(f'SELECT id FROM Services WHERE name="{service["name"]}" AND duration="{service["duration"]}"')
		ids = cursor.fetchall()
		if not ids:
			cursor.execute(f'INSERT INTO Services (name, duration) VALUES ("{service["name"]}", "{service["duration"]}")')
			mydb.commit()
			if not cursor.rowcount:
				print(f'Fail > Servive : {service["name"]} with Duration {service["duration"]}')
			else:
				print(f'Inserted > Servive : {service["name"]} with Duration {service["duration"]}')
		else:
			print(f'In DB => {service["name"]} & {service["duration"]}')

def load_employees(employees):



	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

	for employee in employees:
		cursor.execute(f'SELECT id FROM Users WHERE name="{employee}" AND role="employee"')
		ids = cursor.fetchall()
		if not ids:
			cursor.execute(f'INSERT INTO Users (name, role, timestamp) VALUES ("{employee}", "employee", "{timestamp}")')
			mydb.commit()
			if not cursor.rowcount:
				print(f'Fail > Employee : {employee}')
			else:
				print(f'Inserted > Employee : {employee}')
		else:
			print(f'In DB Employee => {employee}')


def load_holidays(holidays):
	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	# timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

	for holiday in holidays:
		cursor.execute(f'SELECT id FROM Holidays WHERE holiday="{holiday["holiday"]}" AND date="{holiday["date"]}"')
		ids = cursor.fetchall()
		if not ids:
			cursor.execute(f'INSERT INTO Holidays (holiday, date) VALUES ("{holiday["holiday"]}", {holiday["date"]})')
			mydb.commit()
			if not cursor.rowcount:
				print(f'Fail > Holiday : {holiday["holiday"]} ON {holiday["date"]}')
			else:
				print(f'Inserted > Holiday : {holiday["holiday"]} ON {holiday["date"]}')
		else:
			print(f'In DB Employee => {holiday["holiday"]} ON {holiday["date"]}')

def create_user(email, role="customer"):
	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	# date_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
	cursor.execute(f'INSERT INTO Users (name, role, timestamp) VALUES ("{email}", "{role}", "{timestamp}")')
	mydb.commit()

	if not cursor.rowcount:
		print(f'Fail > User : {email} AS {role}')
		return False
	else:
		print(f'Inserted > User : {email} AS {role}')
		cursor.execute(f'SELECT LAST_INSERT_ID()')
		id_ = cursor.fetchone()
		print("id_ = ", id_[0])
		return id_[0]


def initialize():
	cursor = None

	# Validate that DB already exist in not create it
	try:
		cursor = connect_db()
	except Exception:
		if not create_db():
			return [False, "Database Creation Fails"]

	#create all the tables in it exist fail gracefully
	for table, sql in tables_definitions.items():
		mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
		cursor = mydb.cursor()
		try:
			cursor.execute(sql)
		except Exception as error:
			print("Error : ", error)

	# load the initial values for employees and services without duplication
	load_services(initial_services)
	load_employees(initial_employees)
	load_holidays(initial_holidays)



def get_user(req, in_model_req=False):

	sql = None

	if not in_model_req:
		sql = f'SELECT * FROM Users WHERE id="{req.get("id")}"' if req.get("id") else f'SELECT * FROM Users WHERE name="{req.get("email")}"'
	else:
		sql = f'SELECT * FROM Users WHERE name="{req}"'

	if not sql:
		return False

	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	cursor.execute(sql)
	user = cursor.fetchone()

	if not user:
		return False

	return {
		"id": user[0],
		"email": user[1],
		"role": user[2],
		"time": user[3]
	}

def get_users(req):
	sql = None
	queries = {
		"employee": f'SELECT * FROM Users WHERE role="employee"',
		"customer": f'SELECT * FROM Users WHERE role="customer"',
	}

	try:
		sql = queries[req.get("role")]
	except Exception:
		return False

	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	cursor.execute(sql)

	users = [{
		"id": user[0],
		"email": user[1],
		"role": user[2],
		"time": user[3]
	} for user in cursor.fetchall()]


	if not users:
		return False

	return users


def get_services(service_id = None):
	sql = None

	if not service_id:
		sql = f'SELECT * FROM Services'
	else:
		sql = f'SELECT * FROM Services WHERE id={service_id}'

	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	cursor.execute(sql)

	if service_id:
		service = cursor.fetchone()
		return {
			"id": service[0],
			"name": service[1],
			"duration": service[2],
		}

	# users = [{
	# 	"id": user[0],
	# 	"email": user[1],
	# 	"role": user[2],
	# 	"time": user[3]
	# } for user in cursor.fetchall()]


	# if not users:
	# 	return False
	cursor.fetchall()
	return [1,2,4]

def duration_in_secs(duration_str):
	duration_str = duration_str.lower().strip()
	def advancetodigit(strr):
		try:
			while not strr[0].isdigit() and len(strr)>0:
				strr = strr[1:]
		except Exception:
			pass
		return strr if strr else ""

	days = 0
	hours = 0
	mins = 0
	secs = 0

	try:
		if duration_str.index("d") >= 0:
			days = duration_str[:duration_str.index("d")]
			duration_str = duration_str[duration_str.index("d"):]
	except Exception:
		pass

	duration_str = advancetodigit(duration_str)

	try:
		if duration_str.index("h") >= 0:
			h = duration_str.index("h")
			while duration_str[h-1].isdigit() and h-1 >=0:
				h -= 1
			hours = duration_str[h:duration_str.index("h")]
			duration_str = duration_str[duration_str.index("h"):]
	except Exception:
		pass

	duration_str = advancetodigit(duration_str)

	try:
		if duration_str.index("m") >= 0:
			m = duration_str.index("m")
			while duration_str[m-1].isdigit() and m-1 >=0:
				m -= 1
			mins = duration_str[m:duration_str.index("m")]
			duration_str = duration_str[duration_str.index("m"):]
	except Exception:
		pass

	duration_str = advancetodigit(duration_str)

	try:
		if duration_str.index("s") >= 0:
			s = duration_str.index("s")
			while duration_str[s-1].isdigit() and s-1 >=0:
				s -= 1
			secs = duration_str[s:duration_str.index("s")]
	except Exception:
		pass

	return (int(days)*24*60*60 + int(hours)*60*60 + int(mins)*60 + int(secs))


def workorder_setter(start_date, duration_in_secs, service_id, customer_id, employee_id):



	if not duration_in_secs:
		return {"inserted": True, "message": "Inserted WorkOrder"}



	for holiday in initial_holidays:
		date_obj = datetime.strptime(holiday["date"], "%Y-%m-%d")
		if date_obj.strftime("%Y-%m-%d") == start_date.strftime("%Y-%m-%d"):
			# return {"inserted": False, "message": holiday["holiday"]}
			start_date += prime_date.timedelta(days=1)
			start_date = datetime.strptime(start_date.strftime("%Y-%m-%d") + " 9:0:0", "%Y-%m-%d %H:%M:%S")
			workorder_setter(start_date, duration_in_secs, service_id, customer_id, employee_id)




	if start_date.strftime("%A") == "Sunday":
		# return {"inserted": False, "message": "We don't work on Sunday"}
		start_date += prime_date.timedelta(days=1)
		start_date = datetime.strptime(start_date.strftime("%Y-%m-%d") + " 9:0:0", "%Y-%m-%d %H:%M:%S")
		workorder_setter(start_date, duration_in_secs, service_id, customer_id, employee_id)


	last_workorder_sql = f'SELECT * FROM WorkOrders ORDER BY id DESC LIMIT 1'
	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	# last_workorder_sql = f'SELECT TOP 1 * FROM WorkOrders ORDER BY id DESC'

	cursor.execute(last_workorder_sql)
	last_workorder = []
	try:
		last_workorder = cursor.fetchall()[0]
	except Exception:
		pass



	if last_workorder:
		# date_time_last_workorder = datetime.fromisoformat(last_workorder["startTime"]) + prime_date.timedelta(seconds=int(last_workorder["duration"]))
		date_time_last_workorder = datetime.fromisoformat(last_workorder[1]) + prime_date.timedelta(seconds=int(last_workorder[2]))
		
		if date_time_last_workorder >= start_date:
			start_date = date_time_last_workorder + prime_date.timedelta(minutes=1)
	if start_date.hour >= 17:
		start_date += prime_date.timedelta(days=1)
		start_date = datetime.strptime(start_date.strftime("%Y-%m-%d") + " 9:0:0", "%Y-%m-%d %H:%M:%S")


	next_start_time = None
	new_duration = None
	today_last_time = None
	check_remaining_time = start_date + prime_date.timedelta(seconds=duration_in_secs)

	if check_remaining_time.hour >= 17 and check_remaining_time.minute > 0:







		today_last_time = datetime.strptime(start_date.strftime("%Y-%m-%d") + " 17:0:0", "%Y-%m-%d %H:%M:%S") - start_date
		new_duration = duration_in_secs - int(today_last_time.total_seconds())
		next_start_time = start_date + prime_date.timedelta(days=1)
		next_start_time = datetime.strptime(next_start_time.strftime("%Y-%m-%d") + " 9:0:0", "%Y-%m-%d %H:%M:%S")

		sql = f'INSERT INTO WorkOrders (startTime, duration, ServiceId, CustomerId, EmployeeId) VALUES ("{start_date.isoformat()}", "{int(today_last_time.total_seconds())}", "{service_id}", "{customer_id}", "{employee_id}")'

		mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
		cursor = mydb.cursor()
		cursor.execute(sql)
		mydb.commit()

		if not cursor.rowcount:
			print(f'Fail > WorkOrder')
		else:
			print(f'Inserted > WorkOrder')

		workorder_setter(next_start_time, new_duration, service_id, customer_id, employee_id)

	else:



		sql = f'INSERT INTO WorkOrders (startTime, duration, ServiceId, CustomerId, EmployeeId) VALUES ("{start_date.isoformat()}", "{duration_in_secs}", "{service_id}", "{customer_id}", "{employee_id}")'

		mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
		cursor = mydb.cursor()
		cursor.execute(sql)
		mydb.commit()

		if not cursor.rowcount:
			print(f'Fail > WorkOrder')
		else:
			print(f'Inserted > WorkOrder')
			return {"inserted": True, "message": "Inserted WorkOrder"}


def create_workorder(req):
	order_info = {}
	new_workorder = None

	# order_info["startTime"] = datetime.fromisoformat(req.get("startTime").index())


	try:
		order_info["serviceId"] = req.get("serviceId")
		order_info["customer_email"] = req.get("customer_email")
		order_info["employeeId"] = req.get("employeeId")
		order_info["startTime"] = datetime.fromisoformat(req.get("startTime")[:req.get("startTime").index(".")])
	except Exception:
		return {"inserted": False, "message": "Parameter failure"}

	customer = get_user(order_info["customer_email"], True)
	if not customer:
		new_cust_id = create_user(order_info["customer_email"])
		customer = get_user(order_info["customer_email"], True)
		if not customer:
			return {"inserted": False, "message": "Email wasn't created"}

	for holiday in initial_holidays:
		date_obj = datetime.strptime(holiday["date"], "%Y-%m-%d")
		if date_obj.strftime("%Y-%m-%d") == order_info["startTime"].strftime("%Y-%m-%d"):
			return {"inserted": False, "message": holiday["holiday"]}

	if order_info["startTime"].strftime("%A") == "Sunday":
		return {"inserted": False, "message": "We don't work on Sunday"}

	curr_service = get_services(order_info["serviceId"])
	duration_in_secs_ = duration_in_secs(curr_service["duration"])


	# workorder_setter(start_date, duration_in_secs, service_id, customer_id, employee_id):
	return workorder_setter(order_info["startTime"], duration_in_secs_, order_info["serviceId"], customer["id"], order_info["employeeId"])


def get_workorders(req):
	# sql = f'SELECT * FROM WorkOrders INNER JOIN Users u ON u.id=WorkOrders.EmployeeId INNER JOIN Services ON WorkOrders.ServiceId=Services.id INNER JOIN Users ON Users.name="{req.get("email")}"',
	req_date = req.get("date")[:req.get("date").index(".")]

	lower_boundary = datetime.fromisoformat(req_date).strftime("%Y-%m-%d")
	upper_boundary = datetime.fromisoformat(req_date).strftime("%Y-%m-%d")+"T18"

	sql = f'SELECT WorkOrders.*,Services.*,Users.* FROM WorkOrders,Services,Users WHERE WorkOrders.startTime>"{lower_boundary}" AND WorkOrders.startTime<"{upper_boundary}" AND WorkOrders.ServiceId=Services.id AND WorkOrders.EmployeeId=Users.id'
	cust_sql = f'SELECT * FROM Users WHERE name="{req.get("email")}" LIMIT 1'

	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	cursor.execute(sql)
	workorders = cursor.fetchall()

	cursor.execute(cust_sql)
	customer = cursor.fetchone()

	if not customer:
		customer = (create_user(req.get("email")), req.get("email"), "customer")

	return [
		{
            "service": work_order[6],
            "workOrderID": work_order[0],
            "description": work_order[7],
            "start": datetime.fromisoformat(work_order[1]).hour + datetime.fromisoformat(work_order[1]).minute/60,
            "duration": duration_in_secs(work_order[8])/(60*60),
            "employeeId": work_order[9],
            "employee": work_order[10]
        } for work_order in workorders if work_order[4] == customer[0]]


def get_workorders_by_id(req):
	# sql = f'SELECT * FROM WorkOrders INNER JOIN Users u ON u.id=WorkOrders.EmployeeId INNER JOIN Services ON WorkOrders.ServiceId=Services.id INNER JOIN Users ON Users.name="{req.get("email")}"',
	# req_date = req.get("date")[:req.get("date").index(".")]

	# lower_boundary = datetime.fromisoformat(req_date).strftime("%Y-%m-%d")
	# upper_boundary = datetime.fromisoformat(req_date).strftime("%Y-%m-%d")+"T18"

	sql = f'SELECT WorkOrders.*,Services.*,Users.* FROM WorkOrders,Services,Users WHERE WorkOrders.id={req.get("id")} LIMIT 1'

	mydb = mysql.connector.connect(host=db["host"], user=db["user"], password=db["password"], database=db["database"])
	cursor = mydb.cursor()
	cursor.execute(sql)
	workorder = cursor.fetchone()

	if not workorder:
		return False

	cust_sql = f'SELECT * FROM Users WHERE id="{workorder[4]}" LIMIT 1'

	cursor.execute(cust_sql)
	customer = cursor.fetchone()

	if not customer:
		return False

	return {
            "service": workorder[6],
            "workOrderID": workorder[0],
            "description": workorder[7],
            "start": datetime.fromisoformat(workorder[1]).hour + datetime.fromisoformat(workorder[1]).minute/60,
            "duration": duration_in_secs(workorder[8])/(60*60),
            "employeeId": workorder[9],
            "employee": workorder[10],
            "customerId": customer[0],
            "customerEmail": customer[1],
        }



