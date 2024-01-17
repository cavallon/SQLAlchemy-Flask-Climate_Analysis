# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/cjava/OneDrive/Desktop/Challenges/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-18<br/>"
        f"/api/v1.0/2016-08-18/2017-08-18"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    #Query needed precipitation data
    dates_needed = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').all()

    session.close()

    #Convert to a dictionary
    all_prcp = []
    for date, prcp in dates_needed:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    #jsonify results
    return jsonify(all_prcp)


@app.route("/api/v1.0/station")
def station():

    """Return a list of all station names"""
    # Query all station names
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    #jsonify results
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    #Query tobs data
    temp_obs = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-18').all()
    
    session.close()
    
    # Convert list of tuples into normal list
    all_temps = list(np.ravel(temp_obs))

    #jsonify results
    return jsonify(all_temps)

@app.route("/api/v1.0/2016-08-18")
def start():
    #query temp data with needed start date
    temp_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= '2016-08-18').all()
    
    session.close()
    
    # Convert list of tuples into normal list
    temp_range = list(np.ravel(temp_data))

    #jsonify results
    return jsonify(temp_range)

@app.route("/api/v1.0/2016-08-18/2017-08-18")
def startend():
    #query temp with needed start and end dates
    temp_range = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= '2016-08-18').\
        filter(Measurement.date <= '2017-08-18').all()
    
    session.close()
    
    # Convert list of tuples into normal list
    temp_val = list(np.ravel(temp_range))

    #jsonify results
    return jsonify(temp_val)

if __name__ == '__main__':
    app.run(debug=True)