#Importing dependencies

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Set up the database engine for Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect the database in the classes
Base = automap_base()

Base.prepare(engine, reflect=True)

#Create a variable for  each of the classes, in order to reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session link from python to the database
session = Session(engine)

#SETTING UP FLASK

#1. Define the flask app (creates a flask application called "app")
app = Flask(__name__)

#2. Construct the flask routes

#2.1 Welcome route (root or homepage)
    # Todas las rutas deben ir después de definir la app=flask(__name__), de otra forma el código no corre adecuadamente
    # The welcome route is:
@app.route("/")

#2.1.1 Add the routing info for each of the other routes
    #Create a funtion, and returnt the f strings as reference of all the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# 2.2 Create an additional route for the precipitation analysis
@app.route("/api/v1.0/precipitation")

#Create the precipitation() function
def precipitation():

    #code that calcultates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    
    #use jsonify to format the results as a JSON file
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

# 2.3 Create the stations route
# Defining route name
@app.route("/api/v1.0/stations")

#Create a function called stations()
def stations():

#Create a query to get all the stations in the database
    results = session.query(Station.station).all()

    # se usa la función np.ravel  para desenlazar los resultados a un arreglo  de una sola dimensión. "Results" es el parámetro
    # se convierte el resultado en una lista con list ()
    stations = list(np.ravel(results))

   # La lista resultante se presenta en formato JSON
    return jsonify(stations=stations)

# 2.4 Create the temperature observations route
# The goal is to return the temperature observations for the previous year

#Defining route name
@app.route("/api/v1.0/tobs")

#Create a function called temp_monthly()
def temp_monthly():

    #Calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query the primary station fo all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    #Unravel the results into a one-dimension array and covert the array into a list
    temps = list(np.ravel(results))

    #JSONIFY the results
    return jsonify(temps=temps)

# 2.5 Create the statistics route to see the minimum, maximum and average temperatures
# Because we will provide a starting and ending date, this routes are created
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Create a function named stats() with starting and ending parameters
def stats(start=None, end=None):
    
    #Create the query to select the min, max and average temps from the database
    #Create a list called "sel"
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #Adding an "if-not" statement
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
        
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


