from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Vehicle, Driver, Student, Route, FuelRecord

engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/tms")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

vehicle1 = session.query(Vehicle).all()

fuelrec1 = FuelRecord(fuel_type = "Diesel", fuel_cost = "3400", meter_reading = "390",
	date = "01/11/2016", vehicle = vehicle1[0])

fuelrec2 = FuelRecord(fuel_type = "Diesel", fuel_cost = "3400", meter_reading = "390",
	date = "01/11/2016", vehicle = vehicle1[1])

fuelrec3 = FuelRecord(fuel_type = "Diesel", fuel_cost = "3400", meter_reading = "390",
	date = "01/11/2016", vehicle = vehicle1[2])

fuelrec4 = FuelRecord(fuel_type = "Diesel", fuel_cost = "2500", meter_reading = "670",
	date = "03/11/2016", vehicle = vehicle1[0])

fuelrec5 = FuelRecord(fuel_type = "Diesel", fuel_cost = "2500", meter_reading = "670",
	date = "03/11/2016", vehicle = vehicle1[1])

fuelrec6 = FuelRecord(fuel_type = "Diesel", fuel_cost = "2500", meter_reading = "670",
	date = "03/11/2016", vehicle = vehicle1[2])

fuelrec7 = FuelRecord(fuel_type = "Diesel", fuel_cost = "4000", meter_reading = "890",
	date = "04/11/2016", vehicle = vehicle1[0])

fuelrec8 = FuelRecord(fuel_type = "Diesel", fuel_cost = "4000", meter_reading = "890",
	date = "04/11/2016", vehicle = vehicle1[1])

fuelrec9 = FuelRecord(fuel_type = "Diesel", fuel_cost = "4000", meter_reading = "890",
	date = "04/11/2016", vehicle = vehicle1[2])

session.add(fuelrec1)
session.add(fuelrec2)
session.add(fuelrec3)
session.add(fuelrec4)
session.add(fuelrec5)
session.add(fuelrec6)
session.add(fuelrec7)
session.add(fuelrec8)
session.add(fuelrec9)
session.commit()

print "Added all the fuel records!"