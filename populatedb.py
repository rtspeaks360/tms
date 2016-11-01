from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Vehicle, Driver, Student, Route, FuelRecord

engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/tms")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


driver1 = Driver(name = "Rajesh", son_of = "Mahesh", contact = "9382737878",
	address = "123 ambala", license_type = "HMVT", license_number = "HR:012R356543")
session.add(driver1)
session.commit()

driver2 = Driver(name = "Majesh", son_of = "Rahesh", contact = "9382733578",
	address = "456 ambala", license_type = "HMVT", license_number = "HR:012R352533")
session.add(driver2)
session.commit()

driver3 = Driver(name = "Malesh", son_of = "Rakesh", contact = "9334733578",
	address = "4546 ambala", license_type = "HMVT", license_number = "HR:012345663")
session.add(driver3)
session.commit()

route1 = Route(route_number = '1', destination_city = 'Ambala')
session.add(route1)

route2 = Route(route_number = '2', destination_city = 'Chandigarh')
session.add(route2)

route3 = Route(route_number = '3', destination_city = 'Patiala')
session.add(route3)
session.commit()

vehicle1 = Vehicle(vehicle_number = 'HR014564', vehicle_type = 'Bus', model = 'Swaraj Mazada',
	year = '2015', insurance_validity = '01/12/2016', ut_permit_validity = '01/12/2016', haryana_permit_validity = '01/12/2016',
	punjab_permit_validity = '01/12/2016', passenger_tax_paid_upto = '01/12/2016', pollution_certificate_validity = '01/12/2016',
	fitness_valid_upto = '01/12/2016', excise_tax_paid_upto = '01/12/2016', last_service = '01/10/2016', next_service = '01/12/2016',
	last_battery_change = '01/10/2012', driver = driver1, route = route1)
session.add(vehicle1)

vehicle2 = Vehicle(vehicle_number = 'HR019659', vehicle_type = 'Bus', model = 'Swaraj Mazada',
	year = '2014', insurance_validity = '01/12/2016', ut_permit_validity = '01/12/2016', haryana_permit_validity = '01/12/2016',
	punjab_permit_validity = '01/12/2016', passenger_tax_paid_upto = '01/12/2016', pollution_certificate_validity = '01/12/2016',
	fitness_valid_upto = '01/12/2016', excise_tax_paid_upto = '01/12/2016', last_service = '01/10/2016', next_service = '01/12/2016',
	last_battery_change = '01/10/2012', driver = driver2, route = route2)
session.add(vehicle2)

vehicle3 = Vehicle(vehicle_number = 'HR014695', vehicle_type = 'Bus', model = 'Tata',
	year = '2015', insurance_validity = '01/12/2016', ut_permit_validity = '01/12/2016', haryana_permit_validity = '01/12/2016',
	punjab_permit_validity = '01/12/2016', passenger_tax_paid_upto = '01/12/2016', pollution_certificate_validity = '01/12/2016',
	fitness_valid_upto = '01/12/2016', excise_tax_paid_upto = '01/12/2016', last_service = '01/10/2016', next_service = '01/12/2016',
	last_battery_change = '01/10/2012', driver = driver3, route = route3)
session.add(vehicle1)
session.commit()

student1 = Student(name = "Rishabh Thukral", roll_no = '1444268', contact = '9466309992', son_of = 'Mukesh Thukral', branch = 'CSE',
	course = 'BTech', year = '3', college = 'CGC-COE', issue_date = '01/06/2016', end_date = '01/06/2017', route = route1)
session.add(student1)

student2 = Student(name = "Rohit Thukral", roll_no = '1444273', contact = '9466309992', son_of = 'Mukesh Thukral', branch = 'CSE',
	course = 'BTech', year = '3', college = 'CGC-COE', issue_date = '01/06/2016', end_date = '01/06/2017', route = route2)
session.add(student2)

student3 = Student(name = "Rishi Thukral", roll_no = '1443268', contact = '9466309992', son_of = 'Mukesh Thukral', branch = 'CSE',
	course = 'BTech', year = '3', college = 'CGC-COE', issue_date = '01/06/2016', end_date = '01/06/2017', route = route3)
session.add(student1)
session.commit()

print "added items!"