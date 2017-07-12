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
		return render_template('drivernew.html')


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
		return render_template('driveredit.html', driver = r.json()['driver'])	
 

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
		return render_template('driverdelete.html', driver = r.json()['driver'])

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
	if request.method == 'POST':
		new_route = Route(destination_city = request.form['destination_city'],
			route_number = request.form['route_number'])
		session.add(new_route)
		session.commit()

		return redirect(url_for('showRoutes'))
	else:
		return render_template('routenew.html')



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
	editedRoute = session.query(Route).filter(Route.id == route_id).one()
	if request.method == 'POST':
		if request.form['route_number']:
			editedRoute.route_number = request.form['route_number']
		if request.form['destination_city']:
			editedRoute.destination_city = request.form['destination_city']
		session.add(editedRoute)
		session.commit()
		return redirect(url_for('showRoutes'))
	else:
		params = {
			'perform_action' : 'get_route_by_id',
			'id' : route_id
		}
		r = requests.post(API_URL + '/v1/route', data = params)
		return render_template('routeedit.html', route = r.json()['route'])

@app.route('/route/<int:route_id>/delete')
def deleteRoutes(route_id):
	delete_route = session.query(Route).filter(Route.id == route_id).one()
	if request.method == 'POST':
		session.delete(delete_driver)
		session.commit()
		return redirect(url_for('showRoutes'))

	else:
		params = {
			'perform_action' : 'get_route_by_id',
			'id' : route_id
		}
		r = requests.post(API_URL + '/v1/route', data = params)
		return render_template('routedelete.html', route = r.json()['route'])


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
	if request.method == 'POST':
		driver = session.query(Driver).filter(Driver.name == request.form['driver_name']).one()
		route = session.query(Route).filter(Route.route_number == request.form['route_number']).one()
		new_vehicle = Vehicle(vehicle_number = request.form['vehicle_number'], vehicle_type = request.form['vehicle_type'],
			model = request.form['model'], year = request.form['year'], insurance_validity = request.form['insurance_validity'],
			ut_permit_validity = request.form['ut_permit_validity'], haryana_permit_validity = request.form['haryana_permit_validity'],
			punjab_permit_validity = request.form['punjab_permit_validity'], passenger_tax_paid_upto = request.form['passenger_tax_paid_upto'],
			pollution_certificate_validity = request.form['pollution_certificate_validity'], fitness_valid_upto = request.form['fitness_valid_upto'],
			excise_tax_paid_upto = request.form['excise_tax_paid_upto'], last_service = request.form['last_service'], next_service = request.form['next_service'],
			last_battery_change = request.form['last_battery_change'], driver = driver, route = route)
		session.add(new_vehicle)
		session.commit()

		return redirect(url_for('showVehicles'))
	else:
		return render_template('vehiclenew.html')

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
	editedVehicle = session.query(Vehicle).filter(Vehicle.id == vehicle_id).one()
	if request.method == 'POST':
		if request.form['vehicle_number']:
			editedVehicle.vehicle_number = request.form['vehicle_number']
		if request.form['vehicle_type']:
			editedVehicle.vehicle_type = request.form['vehicle_type']
		if request.form['model']:
			editedVehicle.model = request.form['model']
		if request.form['year']:
			editedVehicle.year = request.form['year']
		if request.form['insurance_validity']:
			editedVehicle.insurance_validity = request.form['insurance_validity']
		if request.form['ut_permit_validity']:
			editedVehicle.ut_permit_validity = request.form['ut_permit_validity']
		if request.form['haryana_permit_validity']:
			editedVehicle.haryana_permit_validity = request.form['haryana_permit_validity']
		if request.form['punjab_permit_validity']:
			editedVehicle.punjab_permit_validity = request.form['punjab_permit_validity']
		if request.form['passenger_tax_paid_upto']:
			editedVehicle.passenger_tax_paid_upto = request.form['passenger_tax_paid_upto']
		if request.form['pollution_certificate_validity']:
			editedVehicle.pollution_certificate_validity = request.form['pollution_certificate_validity']
		if request.form['fitness_valid_upto']:
			editedVehicle.fitness_valid_upto = request.form['fitness_valid_upto']
		if request.form['excise_tax_paid_upto']:
			editedVehicle.excise_tax_paid_upto = request.form['excise_tax_paid_upto']
		if request.form['last_service']:
			editedVehicle.last_service = request.form['last_service']
		if request.form['next_service']:
			editedVehicle.next_service = request.form['next_service']
		if request.form['last_battery_change']:
			editedVehicle.last_battery_change = request.form['last_battery_change']
		if request.form['driver_name']:
			driver = session.query(Driver).filter(Driver.name == request.form['driver_name']).one()
			editedDriver.driver = driver
		if request.form['route_number']:
			route = session.query(Route).filter(Route.route_number == request.form['route_number'])
			editedVehicle.route = route
		session.add(editedVehicle)
		session.commit()
		return redirect(url_for('showVehicles'))
	else:
		params = {
			'perform_action' : 'get_vehicle_by_id',
			'id' : vehicle_id
		}
		r = requests.post(API_URL + '/v1/vehicle', data = params)
		return render_template('vehicleedit.html', vehicle = r.json()['vehicle'])


@app.route('/vehicle/<int:vehicle_id>/delete')
def deleteVehicle(vehicle_id):
	delete_vehicle = session.query(Vehicle).filter(Vehicle.id == vehicle_id).one()
	if request.method == 'POST':
		session.delete(delete_driver)
		session.commit()
		return redirect(url_for('showVehicles'))

	else:
		params = {
			'perform_action' : 'get_vehicle_by_id',
			'id' : vehicle_id
		}
		r = requests.post(API_URL + '/v1/vehicle', data = params)
		return render_template('vehicledelete.html', route = r.json()['vehicle'])

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
	if request.method == 'POST':
		route = session.query(Route).filter(Route.route_number == request.form['route_number']).one()
		new_student = Student(name = request.form['name'], roll_no = request.form['roll_no'], contact = request.form['contact'], 
			son_of = request.form['son_of'], branch = request.form['branch'], course = request.form['course'], year = request.form['year'],
			college = request.form['college'], issue_date = request.form['issue_date'], end_date = request.form['end_date'], route = route)
		session.add(new_student)
		session.commit()

		return redirect(url_for('showStudents'))
	else:
		return render_template('studentnew.html')


@app.route('/student/<int:student_id>')
def showStudentDetails(student_id):
	params = {
		'perform_action' : 'get_student_by_id',
		'id' : student_id
	}
	r = requests.post(API_URL + '/v1/student', data = params)
	return render_template('studentdetails.html', student = r.json()['student'])

@app.route('/student/<int:student_id>/edit')
def editStudents(student_id):
	editedStudent = session.query(Student).filter(Student.id == student_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedStudent.name = request.form['name']
		if request.form['roll_no']:
			editedStudent.roll_no = request.form['roll_no']
		if request.form['contact']:
			editedStudent.contact = request.form['contact']
		if request.form['son_of']:
			editedStudent.son_of = request.form['son_of']
		if request.form['branch']:
			editedStudent.branch = request.form['branch']
		if request.form['course']:
			editedStudent.course = request.form['course']
		if request.form['year']:
			editedStudent.year = request.form['year']
		if request.form['college']:
			editedStudent.college = request.form['college']
		if request.form['issue_date']:
			editedStudent.issue_date = request.form['issue_date']
		if request.form['end_date']:
			editedStudent.end_date = request.form['end_date']
		if request.form['route_number']:
			route = session.query(Route).filter(Route.route_number == request.form['route_number']).one()
			editedStudent.route = route
		session.add(editedStudent)
		session.commit()
		return redirect(url_for('showStudents'))
	else:
		params = {
			'perform_action' : 'get_student_by_id',
			'id' : student_id
		}
		r = requests.post(API_URL + '/v1/student', data = params)
		return render_template('studentedit.html', student = r.json()['student'])


@app.route('/student/<int:student_id>/delete')
def deleteStudents(student_id):
	delete_student = session.query(Student).filter(Student.id == student_id).one()
	if request.method == 'POST':
		session.delete(delete_student)
		session.commit()
		return redirect(url_for('showStudents'))

	else:
		params = {
			'perform_action' : 'get_student_by_id',
			'id' : student_id
		}
		r = requests.post(API_URL + '/v1/student', data = params)
		return render_template('studentdelete.html', student = r.json()['student'])

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
	if request.method == 'POST':
		vehicle = session.query(Vehicle).filter(Vehicle.vehicle_number == request.form['vehicle_number'])
		new_fuelrec = FuelRecord(fuel_type = request.form['fuel_type'], fuel_cost = request.form['fuel_cost'],
		meter_reading = request.form['meter_reading'], date = request.form["date"], vehicle = vehicle)
		session.add(new_fuelrec)
		session.commit()

		return redirect(url_for('showFuelRecords'))
	else:
		return render_template('fuelrecordnew.html')

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
	editedfuelrec = session.query(Vehicle).filter(Vehicle.id == fuel_record_id).one()
	if request.method == 'POST':
		if request.form['vehicle_number']:
			vehicle = session.query(Vehicle).filter(Vehicle.vehicle_number == request.form['vehicle_number'])
			editedfuelrec.vehicle = vehicle
		if request.form['fuel_type']:
			editedfuelrec.fuel_type = request.form['fuel_type']
		if request.form['fuel_cost']:
			editedfuelrec.fuel_cost = request.form['fuel_cost']
		if request.form['meter_reading']:
			editedfuelrec.meter_reading = request.form['meter_reading']
		if request.form['date']:
			editedfuelrec.date = request.form['date']
		session.add(editedfuelrec)
		session.commit()
		return redirect(url_for('showFuelRecords'))
	else:
		params = {
			'perform_action' : 'get_fuelrec_by_id',
			'id' : fuel_record_id
		}
		r = requests.post(API_URL + '/v1/fuelrecs', data = params)
		return render_template('fuelrecordedit.html', fuelrec = r.json()['fuelrec'])


@app.route('/fuel_records/<int:fuel_record_id>/delete')
def deleteFuelRecords(fuel_record_id):
	delete_fuelrec = session.query(FuelRecord).filter(FuelRecord.id == fuel_record_id).one()
	if request.method == 'POST':
		session.delete(delete_fuelrec)
		session.commit()
		return redirect(url_for('showFuelRecords'))

	else:
		params = {
			'perform_action' : 'get_fuelrec_by_id',
			'id' : fuel_record_id
		}
		r = requests.post(API_URL + '/v1/fuelrecs', data = params)
		return render_template('fuelrecorddelete.html', route = r.json()['fuelrec'])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)