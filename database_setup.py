# importing dependencies.
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# declaring an object of the declarative base class.
Base = declarative_base()

# Various models for application support. 
class Student(Base):

	"""Provides the structure for students table in the database."""

	__tablename__ = "students"

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	roll_no = Column(Integer, nullable = False)
	contact = Column(String(12), nullable = False)
	son_of = Column(String(80), nullable = False)
	branch = Column(String(40), nullable = False)
	course = Column(String(40), nullable = False)
	year = Column(Integer, nullable = False)
	college = Column(String(50), nullable = False) 
	issue_date = Column(String(10), nullable = False)
	end_date = Column(String(10), nullable = False)

	route_id = Column(Integer, ForeignKey('routes.id'))
	route = relationship("Route", back_populates = "students")

class Driver(Base):

	"""Provides the structure for the drivers table in the database."""

	__tablename__ = "drivers"

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	son_of = Column(String(80), nullable = False)
	contact = Column(String(12), nullable = False)
	address = Column(String(80), nullable = False)
	license_type = Column(String(10), nullable = False)
	license_number = Column(String(20), nullable = False)

	vehicle_assigned = relationship("Vehicle", uselist = False, back_populates = "driver")

class Route(Base):

	"""Provides the structure for the routes table in the database."""

	__tablename__ = "routes"

	id = Column(Integer, primary_key = True)
	route_number = Column(Integer, nullable = False)
	destination_city = Column(String(20), nullable = False)

	students = relationship("Student", back_populates = "route")
	
	vehicle_assigned = relationship("Vehicle", uselist = False, back_populates = "route")

class FuelRecord(Base):
	
	"""Provides the structure for the fuel records table in the database."""

	__tablename__ = "fuel_records"

	id = Column(Integer, primary_key = True)
	fuel_type = Column(String(10), nullable = False)
	fuel_cost = Column(Integer, nullable = False)
	meter_reading = Column(Integer, nullable = False)
	date = Column(String(10), nullable = False)
	
	vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
	vehicle = relationship("Vehicle", back_populates = "fuel_records")

class Vehicle(Base):

	"""Provides the structure for the vehicles table in the database."""

	__tablename__ = "vehicles"

	id =  Column(Integer, primary_key = True)
	vehicle_number = Column(String(10), nullable = False)
	vehicle_type = Column(String(10), nullable =False)
	model = Column(String(40), nullable = False)
	year = Column(String(4), nullable = False)
	insurance_validity = Column(String(10), nullable = False)
	ut_permit_validity = Column(String(10), nullable = False)
	haryana_permit_validity = Column(String(10), nullable = False)
	punjab_permit_validity = Column(String(10), nullable = False)
	passenger_tax_paid_upto = Column(String(10), nullable = False)
	pollution_certificate_validity = Column(String(10), nullable = False)
	fitness_valid_upto = Column(String(10), nullable = False)
	excise_tax_paid_upto = Column(String(10), nullable = False)
	last_service = Column(String(10), nullable = False)
	next_service = Column(String(10), nullable = False)
	last_battery_change = Column(String(10), nullable = False)

	driver_id = Column(Integer, ForeignKey("drivers.id"))
	driver = relationship("Driver", back_populates = "vehicle_assigned")

	route_id = Column(Integer, ForeignKey("routes.id"))
	route = relationship("Route", back_populates = "vehicle_assigned")

	fuel_records = relationship("FuelRecord", back_populates = "vehicle")


# Making a database engine
engine = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/tms")

Base.metadata.create_all(engine)