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
	return "Edit Driver page!"

@app.route('/driver/<int:driver_id>/delete')
def deleteDrivers(driver_id):
	return "Delete drivers page!"

@app.route('/vehicle')
def showVehicles():
	return "vehicles Page!"

@app.route('/vehicle/new')
def addVehicles():
	return "Add new vehicle page"

@app.route('/vehicle/<int:vehicle_id>')
def showVehicleetails():
	return "Vehicle Details Page!"

@app.route('/vehicle/<int:vehicle_id>/edit')
def editVehicle(vehicle_id):
	return "Edit vehicle page!"

@app.route('/vehicle/<int:vehicle_id>/delete')
def deleteVehicle(vehicle_id):
	return "Delete vehicles page!"

@app.route('/student')
def showStudents():
	return "students Page!"

@app.route('/student/new')
def addStudents():
	return "Add new student page"

@app.route('/student/<int:student_id>/edit')
def editStudents(student_id):
	return "Edit student page!"

@app.route('/student/<int:student_id>/delete')
def deleteStudents(student_id):
	return "Delete students page!"

@app.route('/route')
def showRoutes():
	return "routes Page!"

@app.route('/route/new')
def addRoutes():
	return "Add new route page"

@app.route('/route/<int:route_id>/edit')
def editRoutes(route_id):
	return "Edit route page!"

@app.route('/route/<int:route_id>/delete')
def deleteRoutes(route_id):
	return "Delete routes page!"

@app.route('/fuel_records')
def showFuelRecords():
	return "fuel_recordss Page!"

@app.route('/fuel_records/new')
def addFuelRecords():
	return "Add new fuel_records page"

@app.route('/fuel_records/<int:fuel_records_id>/edit')
def editFuelRecords(fuel_records_id):
	return "Edit fuel_records page!"

@app.route('/fuel_records/<int:fuel_records_id>/delete')
def deleteFuelRecords(fuel_records_id):
	return "Delete fuel_recordss page!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)