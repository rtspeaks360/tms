import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Vehicle, Driver, Student, Route, FuelRecord

API_URL = "http://127.0.0.1:8000"

app = Flask(__name__)

engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/tms")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/index')
def homePage():
	params = {
		'perform_action' : 'homepage_values',
	}
	#return "Home Page!"
	r = requests.post(API_URL + '/v1/homepage', data = params)
	print r.json()
	values = r.json()['homepage_values'] 
	return render_template('index.html', homepage_values = values)
	# return "homepage"

@app.route('/driver')
def showDrivers():
	params = {
		'perform_action' : 'get_all_drivers'
	}
	r = requests.post(API_URL + '/v1/driver', data = params)
	
	# print r.json()
	all_drivers = r.json()['drivers']
	# print all_drivers
	return render_template('drivers.html', drivers = all_drivers)

@app.route('/driver/new', methods = ['GET', 'POST'])
def addDrivers():
	if request.method == 'POST':
		new_driver = Driver(name = request.form['name'], son_of = request.form['son_of'], 
			contact = request.form['contact'], address = request.form['address'],
			license_type = request.form['license_type'], license_number = request.form['license_number'])
		session.add(new_driver)
		session.commit()

		return redirect(url_for('showDrivers'))
	else:
		return render_template('newdriver.html')
	return render_template('newdriver.html')

@app.route('/driver/<int:driver_id>')
def showDriverDetails(driver_id):
	params = {
		'perform_action' : 'get_driver_by_id',
		'id' : driver_id
	}
	r = requests.post(API_URL + '/v1/driver', data = params)
	return render_template('driverdetails.html', driver = r.json()['driver'])

@app.route('/driver/<int:driver_id>/edit', methods = ['GET', 'POST'])
def editDrivers(driver_id):
	driver1 = Driver(name = "Rajesh", son_of = "Mahesh", contact = "9382737878",
	address = "123 ambala", license_type = "HMVT", license_number = "HR:012R356543")
	editedDriver = session.query(Driver).filter(Driver.id == driver_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedDriver.name = request.form['name']
		if request.form['son_of']:
			editedDriver.son_of = request.form['son_of']
		if request.form['contact']:
			editedDriver.contact = request.form['contact']
		if request.form['address']:
			editedDriver.address = request.form['address']
		if request.form['license_type']:
			editedDriver['license_type'] = request.form['license_type']
		if request.form['license_number']:
			editedDriver['license_number'] = request.form['license_number']
		session.add(editedDriver)
		session.commit()
		return redirect(url_for('showDrivers'))
	else:
		params = {
			'perform_action' : 'get_driver_by_id',
			'id' : driver_id
		}
		r = requests.post(API_URL + '/v1/driver', data = params)
		return render_template('editdriver.html', driver = r.json()['driver'])	
 

@app.route('/driver/<int:driver_id>/delete', methods = ['GET', 'POST'])
def deleteDrivers(driver_id):
	delete_driver = session.query(Driver).filter(Driver.id == driver_id).one()
	if request.method == 'POST':
		session.delete(delete_driver)
		session.commit()
		return redirect(url_for('showDrivers'))

	else:
		params = {
			'perform_action' : 'get_driver_by_id',
			'id' : driver_id
		}
		r = requests.post(API_URL + '/v1/driver', data = params)
		return render_template('deletedriver.html', driver = r.json()['driver'])

@app.route('/route')
def showRoutes():
	params = {
		'perform_action' : 'get_all_routes'
	}
	r = requests.post(API_URL + '/v1/route', data = params)
	
	# print r.json()
	all_routes = r.json()['routes']
	# print all_drivers
	return render_template('routes.html', routes = all_routes)

@app.route('/route/new')
def addRoutes():
	return "Add new route page"

@app.route('/route/<int:route_id>')
def showRouteDetails(route_id):
	params = {
		'perform_action' : 'get_route_by_id',
		'id' : route_id
	}
	r = requests.post(API_URL + '/v1/route', data = params)
	return render_template('routedetails.html', route = r.json()['route'])

@app.route('/route/<int:route_id>/edit')
def editRoutes(route_id):
	return "Edit route page!"

@app.route('/route/<int:route_id>/delete')
def deleteRoutes(route_id):
	return "Delete routes page!"

@app.route('/vehicle')
def showVehicles():
	params = {
		'perform_action' : 'get_all_vehicles'
	}
	r = requests.post(API_URL + '/v1/vehicle', data = params)
	
	# print r.json()
	all_vehicles = r.json()['vehicles']
	# print all_drivers
	return render_template('vehicles.html', vehicles = all_vehicles)
	

@app.route('/vehicle/new')
def addVehicles():
	return "Add new vehicle page"

@app.route('/vehicle/<int:vehicle_id>')
def showVehicleDetails(vehicle_id):
	params = {
		'perform_action' : 'get_vehicle_by_id',
		'id' : vehicle_id
	}
	r = requests.post(API_URL + '/v1/vehicle', data = params)
	return render_template('vehicledetails.html', vehicle = r.json()['vehicle'])

@app.route('/vehicle/<int:vehicle_id>/edit')
def editVehicle(vehicle_id):
	return "Edit vehicle page!"

@app.route('/vehicle/<int:vehicle_id>/delete')
def deleteVehicle(vehicle_id):
	return "Delete vehicles page!"

@app.route('/student')
def showStudents():
	params = {
		'perform_action' : 'get_all_students'
	}
	r = requests.post(API_URL + '/v1/student', data = params)
	
	# print r.json()
	all_students = r.json()['students']
	# print all_drivers
	return render_template('students.html', students = all_students)

@app.route('/student/new')
def addStudents():
	return "Add new student page"

@app.route('/student/<int:student_id>')
def showStudentDetails():
	params = {
		'perform_action' : 'get_student_by_id',
		'id' : student_id
	}
	r = requests.post(API_URL + '/v1/student', data = params)
	return render_template('studentdetails.html', student = r.json()['student'])

@app.route('/student/<int:student_id>/edit')
def editStudents(student_id):
	return "Edit student page!"

@app.route('/student/<int:student_id>/delete')
def deleteStudents(student_id):
	return "Delete students page!"

@app.route('/fuel_records')
def showFuelRecords():
	params = {
		'perform_action' : 'get_all_fuelrecs'
	}
	r = requests.post(API_URL + '/v1/fuelrecs', data = params)
	
	# print r.json()
	all_fuelrecs = r.json()['fuelrecs']
	# print all_drivers
	return render_template('fuelrecords.html', fuelrecs = all_fuelrecs)

@app.route('/fuel_records/new')
def addFuelRecords():
	return "Add new fuel_records page"

@app.route('/fuel_records/<int:fuel_record_id>')
def showFuelRecordDetails(fuel_record_id):
	params = {
		'perform_action' : 'get_fuelrec_by_id',
		'id' : fuel_record_id
	}
	r = requests.post(API_URL + '/v1/fuelrecs', data = params)
	return render_template('fuelrecorddetails.html', fuelrec = r.json()['fuelrec'])	

@app.route('/fuel_records/<int:fuel_record_id>/edit')
def editFuelRecords(fuel_record_id):
	return "Edit fuel_records page!"

@app.route('/fuel_records/<int:fuel_record_id>/delete')
def deleteFuelRecords(fuel_record_id):
	return "Delete fuel_recordss page!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)