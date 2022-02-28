from flask import Flask, jsonify

# import sqlalchemy dependencies
import numpy as np
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# DB Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
# Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Surfs Up Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the annual rainfall in hawaii data as json"""


    # get prcp_results
    # Design a query to retrieve the last 12 months of precipitation data and plot the results.
    # Starting from the most recent data point in the database.
    # Calculate the date one year from the last date in data set.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prev_year

    # Perform a query to retrieve the data and precipitation scores for prev_year
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    prcp_results

    #close session
    session.close()

    # create dict with date: prcp
    yearly_prcp = {date: prcp for date, prcp in prcp_results}

    return jsonify(yearly_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Returns Stations """

    station_results= session.query(Station.station).all()

    #close session
    session.close()

    #unravel this list
    stations = list(np.ravel(station_results))


    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """"Returns Temperature"""

    #Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram

    year_before = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_result = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_before).all()

    #close session
    session.close()

    # unravel results
    temps = list(np.ravel(tobs_result))

    return jsonify(temps=temps)


if __name__ == "__main__":
    app.run(debug=True)
