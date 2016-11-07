import json
import datetime
from flask import Flask, jsonify, request
from flask import request
import flask_restful
from flask.ext import restful
from flask.ext.restful import reqparse
from flask.ext.cors import CORS
from collections import OrderedDict
from sets import Set
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Vehicle, Driver, Student, Route, FuelRecord

engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/tms")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

application = Flask(__name__)
CORS(application)
api = flask_restful.Api(application)

class DriverAPI(restful.Resource):
	def post(self):
		args = request_args1.parse_args()
		
		if args['perform_action'] == "get_all_drivers":
			drivers_query_result = session.query(Driver).all()
			drivers = []
			for d in drivers_query_result:
				drivers.append(d.serialize)
			print drivers
			return jsonify(drivers = drivers)

		if args['perform_action'] == 'get_driver_by_id':
			drivers_query_result = session.query(Driver).filter(Driver.id == args['id']).one()
			return jsonify(driver = drivers_query_result.serialize)

		if args['perform_action'] == 'add_driver':
			new_driver = Driver(name = args['name'], son_of = args['son_of'], contact = args['contact'],
				address = args['address'], license_type = args['license_type'], license_number = args['license_number'])
			session.add(new_driver)
			session.commit()
			return jsonify(message = "New Driver Created")

		if args['perform_action'] == 'delete_driver':
			driver = session.query(Driver).filter(Driver.id == args['id']).one()
			session.delete(driver)
			session.commit()
			return jsonify(message = "Driver Deleted")

		if args['perform_action'] == "update_driver":
			driver = session.query(Driver).filter(Driver.id == args[id]).one()
			session.delete(driver)
			updated_driver = Driver(id = args['id'], name = args['name'], son_of = args['son_of'], contact = args['contact'],
				address = args['address'], license_type = args['license_type'], license_number = args['license_number'])
			session.add(updated_driver)
			session.commit()
			return jsonify(message = "Driver updated")

class RouteAPI(restful.Resource):
	def post(self):
		args = request_args2.parse_args()

		if args['perform_action'] == "get_all_routes":
			routes_query_result = session.query(Route).all()
			routes = []
			for r in routes_query_result:
				routes.append(r.serialize)
			return jsonify(routes = routes)

		if args['perform_action'] == 'get_route_by_id':
			route_query_result = session.query(Route).filter(Route.id == args['id']).one()
			route = route_query_result.serialize
			route['number_of_students'] = len(session.query(Student).filter(Student.route_id == args['id']).all())
			return jsonify(route  = route)

		if args['perform_action'] == 'add_route':
			new_route = Route(route_number = args['route_number'], destination_city = args['destination_city'])
			session.add(new_route)
			session.commit()
			return jsonify(message = "New Route Created")

		if args['perform_action'] == 'delete_route':
			route = session.query(Route).filter(Route.id == args['id']).one()
			session.delete(route)
			session.commit()
			return jsonify(message = "Route Deleted")

		if args['perform_action'] == "update_route":
			route = session.query(Route).filter(Route.id == args[id]).one()
			session.delete(route)
			updated_route = Route(id = args['id'], route_number = args['route_number'], destination_city = args['destination_city'])
			session.add(updated_route)
			session.commit()
			return jsonify(message = "Route updated")

class StudentAPI(restful.Resource):
	def post(self):
		args = request_args3.parse_args()

		if args['perform_action'] == "get_all_students":
			print "students api"
			students_query_result = session.query(Student).all()
			print students_query_result
			students = []
			for s in students_query_result:
				students.append(s.serialize)
			return jsonify(students = students)

		if args['perform_action'] == 'get_student_by_id':
			student_query_result = session.query(Student).filter(Student.id == args['id']).one()
			student = student_query_result.serialize
			return jsonify(student  = student)

		if args['perform_action'] == 'add_student':
			route_of_student = session.query(Route).filter(Route.route_number == args['route_number']).one()
			student = Student(name = args['name'], roll_no = args['roll_no'], contact = args['contact'], son_of = args['son_of'], branch = args['branch'],
				course = args['course'], year = args['year'], college = args['college'], issue_date = args['issue_date'], end_date = args['end_date'], route = route_of_student)
			session.add(student)
			session.commit()
			return jsonify(message = "New student Created")

		if args['perform_action'] == 'delete_student':
			student = session.query(Student).filter(Student.id == args['id']).one()
			session.delete(student)
			session.commit()
			return jsonify(message = "Student Deleted")

		if args['perform_action'] == "update_student":
			student = session.query(Student).filter(Student.id == args[id]).one()
			session.delete(student)
			route_of_student = session.query(Route).filter(Route.route_number == args['route_number']).one()
			student = Student(name = args['name'], roll_no = args['roll_no'], contact = args['contact'], son_of = args['son_of'], branch = args['branch'],
				course = args['course'], year = args['year'], college = args['college'], issue_date = args['issue_date'], end_date = args['end_date'], route = route_of_student)
			session.add(student)
			session.commit()
			return jsonify(message = "Student updated")

class VehicleAPI(restful.Resource):
	def post(self):
		args = request_args4.parse_args()

		if args['perform_action'] == "get_all_vehicles":
			vehicles_query_result = session.query(Vehicle).all()
			vehicles = []
			for v in vehicles_query_result:
				vehicles.append(v.serialize)
			return jsonify(vehicles = vehicles)

		if args['perform_action'] == 'get_vehicle_by_id':
			vehicle_query_result = session.query(Vehicle).filter(Vehicle.id == args['id']).one()
			vehicle = vehicle_query_result.serialize
			return jsonify(vehicle  = vehicle)

		if args['perform_action'] == 'add_vehicle':
			driver_of_vehicle = session.query(Driver).filter(Driver.name == args['driver_name']).one()
			route_of_vehicle = session.query(Route).filter(Route.route_number == args['route_number']).one()
			vehicle = Vehicle(vehicle_number = args['vehicle_number'], vehicle_type = args['vehicle_type'], model = args['model'],
				year = args['year'], insurance_validity = args['insurance_validity'], ut_permit_validity = args['ut_permit_validity'],
				haryana_permit_validity = args['haryana_permit_validity'], punjab_permit_validity = args['punjab_permit_validity'],
				passenger_tax_paid_upto = args['passenger_tax_paid_upto'], pollution_certificate_validity = args['pollution_certificate_validity'],
				fitness_valid_upto = args['fitness_valid_upto'], excise_tax_paid_upto = args['excise_tax_paid_upto'], last_service = args['last_service'],
				next_service = args['next_service'], last_battery_change = args['last_battery_change'], driver = driver_of_vehicle, route = route_of_vehicle)
			session.add(vehicle)
			session.commit()
			return jsonify(message = "New vehicle Created")

		if args['perform_action'] == 'delete_vehicle':
			vehicle = session.query(Vehicle).filter(Vehicle.id == args['id']).one()
			session.delete(vehicle)
			session.commit()
			return jsonify(message = "Vehicle Deleted")

		if args['perform_action'] == "update_vehicle":
			vehicle = session.query(Vehicle).filter(Vehicle.id == args[id]).one()
			session.delete(vehicle)
			driver_of_vehicle = session.query(Driver).filter(Driver.name == args['driver_name']).one()
			route_of_vehicle = session.query(Route).filter(Route.route_number == args['route_number']).one()
			vehicle = Vehicle(vehicle_number = args['vehicle_number'], vehicle_type = args['vehicle_type'], model = args['model'],
				year = args['year'], insurance_validity = args['insurance_validity'], ut_permit_validity = args['ut_permit_validity'],
				haryana_permit_validity = args['haryana_permit_validity'], punjab_permit_validity = args['punjab_permit_validity'],
				passenger_tax_paid_upto = args['passenger_tax_paid_upto'], pollution_certificate_validity = args['pollution_certificate_validity'],
				fitness_valid_upto = args['fitness_valid_upto'], excise_tax_paid_upto = args['excise_tax_paid_upto'], last_service = args['last_service'],
				next_service = args['next_service'], last_battery_change = args['last_battery_change'], driver = driver_of_vehicle, route = route_of_vehicle)
			session.add(vehicle)
			session.commit()
			return jsonify(message = "vehicle updated")

class HomeAPI(restful.Resource):
	def post(self):
		args = request_args5.parse_args()

		if args['perform_action'] == 'homepage_values':
			values = {}
			vehicle = len(session.query(Vehicle).all())
			values['vehicles'] = vehicle
			values['students'] = len(session.query(Student).all())
			values['drivers'] = len(session.query(Driver).all())
			values['routes'] = len(session.query(Route).all())
			values['fuelrecs'] = len(session.query(FuelRecord).all())
			fuelrecs = session.query(FuelRecord).all()
			cost = 0
			for f in fuelrecs:
				cost = cost + f.fuel_cost   
			values['fuelrecs_weekly'] = cost
			values['fuelrecs_monthly'] = cost
			values['fuelrecs_quaterly'] = cost
			return jsonify(homepage_values = values)

class FuelRecordAPI(restful.Resource):
	def post(self):
		args = request_args6.parse_args()

		if args['perform_action'] == "get_all_fuelrecs":
			fuelrecs_query_result = session.query(FuelRecord).all()
			fuelrecs = []
			for f in fuelrecs_query_result:
				fuelrecs.append(f.serialize)
			return jsonify(fuelrecs = fuelrecs)

		if args['perform_action'] == "get_fuelrec_by_id":
			fuelrec_query_result = session.query(FuelRecord).filter(FuelRecord.id == args['id']).one()
			fuelrec = fuelrec_query_result.serialize
			return jsonify(fuelrec  = fuelrec)

		if args['perform_action'] == "add_fuelrec":
			vehicle = session.query(Vehicle).filter(Vehicle.vehicle_number == args['vehicle_number']).one()
			fuelrec = FuelRecord(fuel_type = args['fuel_type'], fuel_cost = args['fuel_cost'],
				meter_reading = args['meter_reading'], date = args['date'], vehicle = vehicle)
			session.add(fuelrec)
			session.commit()
			return jsonify(message = "fuelrec added")

		if args['perform_action'] == "delete_fuelrec":
			fuelrec = session.query(FuelRecord).filter(FuelRecord.id == args['id']).one()
			session.delete(fuelrec)
			session.commit()
			return jsonify(message = "fuelrec Deleted")			


api.add_resource(FuelRecordAPI, '/v1/fuelrecs')
request_args6 = reqparse.RequestParser(bundle_errors = True)
request_args6.add_argument('perform_action', type = str, required = True, location = 'form')
request_args6.add_argument('id', type = str, required = False, location = 'form')
request_args6.add_argument('fuel_type', type = str, required = False, location = 'form')
request_args6.add_argument('fuel_cost', type = str, required = False, location = 'form')
request_args6.add_argument('meter_reading', type = str, required = False, location = 'form')
request_args6.add_argument('date', type = str, required = False, location = 'form')
request_args6.add_argument('vehicle_number', type = str, required = False, location = 'form')

api.add_resource(HomeAPI, '/v1/homepage')
request_args5 = reqparse.RequestParser(bundle_errors = True)
request_args5.add_argument('perform_action', type = str, required = True, location = 'form')

api.add_resource(VehicleAPI, '/v1/vehicle')
request_args4 = reqparse.RequestParser(bundle_errors=True)
request_args4.add_argument('perform_action', type = str, required = True, location = 'form')
request_args4.add_argument('id', type = str, required = False, location = 'form')
request_args4.add_argument('vehicle_number', type = str, required = False, location = 'form')
request_args4.add_argument('vehicle_type', type = str, required = False, location = 'form')
request_args4.add_argument('model', type = str, required = False, location = 'form')
request_args4.add_argument('year', type = str, required = False, location = 'form')
request_args4.add_argument('insurance_validity', type = str, required = False, location = 'form')
request_args4.add_argument('ut_permit_validity', type = str, required = False, location = 'form')
request_args4.add_argument('haryana_permit_validity', type = str, required = False, location = 'form')
request_args4.add_argument('punjab_permit_validity', type = str, required = False, location = 'form')
request_args4.add_argument('passenger_tax_paid_upto', type = str, required = False, location = 'form')
request_args4.add_argument('pollution_certificate_validity', type = str, required = False, location = 'form')
request_args4.add_argument('fitness_valid_upto', type = str, required = False, location = 'form')
request_args4.add_argument('excise_tax_paid_upto', type = str, required = False, location = 'form')
request_args4.add_argument('last_service', type = str, required = False, location = 'form')
request_args4.add_argument('next_service', type = str, required = False, location = 'form')
request_args4.add_argument('last_battery_change', type = str, required = False, location = 'form')
request_args4.add_argument('driver_name', type = str, required = False, location = 'form')
request_args4.add_argument('route_number', type = str, required = False, location = 'form')

api.add_resource(StudentAPI, '/v1/student')
request_args3 = reqparse.RequestParser(bundle_errors=True)
request_args3.add_argument('perform_action', type = str, required = True, location = 'form')
request_args3.add_argument('id', type = str, required = False, location = 'form')
request_args3.add_argument('name', type = str, required = False, location = 'form')
request_args3.add_argument('roll_no', type = str, required = False, location = 'form')
request_args3.add_argument('contact', type = str, required = False, location = 'form')
request_args3.add_argument('son_of', type = str, required = False, location = 'form')
request_args3.add_argument('branch', type = str, required = False, location = 'form')
request_args3.add_argument('course', type = str, required = False, location = 'form')
request_args3.add_argument('year', type = str, required = False, location = 'form')
request_args3.add_argument('college', type = str, required = False, location = 'form')
request_args3.add_argument('issue_date', type = str, required = False, location = 'form')
request_args3.add_argument('end_date', type = str, required = False, location = 'form')
request_args3.add_argument('route_number', type = str, required = False, location = 'form')

api.add_resource(RouteAPI, '/v1/route')
request_args2 = reqparse.RequestParser(bundle_errors=True)
request_args2.add_argument('perform_action', type = str, required = True, location = 'form')
request_args2.add_argument('id', type = str, required = False, location = 'form')
request_args2.add_argument('route_number', type = str, required = False, location = 'form')
request_args2.add_argument('destination_city', type = str, required = False, location = 'form')

api.add_resource(DriverAPI,'/v1/driver')
request_args1 = reqparse.RequestParser(bundle_errors=True)
request_args1.add_argument('perform_action', type = str, required = True, location = 'form')
request_args1.add_argument('id', type = str, required = False, location = 'form')
request_args1.add_argument('name', type = str, required = False, location = 'form')
request_args1.add_argument('son_of', type = str, required = False, location = 'form')
request_args1.add_argument('contact', type = str, required = False, location = 'form')
request_args1.add_argument('address', type = str, required = False, location = 'form')
request_args1.add_argument('license_type', type = str, required = False, location = 'form')
request_args1.add_argument('license_number', type = str, required = False, location = 'form')

@application.after_request
def after_request(response):
    response.headers.add("Content-type", "application/json");
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == "__main__":
  application.debug = True
  application.run(host = '0.0.0.0', port = 8000)