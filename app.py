import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

# Setup the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

Base = automap_base()

Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create session from python to DB
session = Session(engine)


#setup flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"<p>Welcome to the Hawaii weather API!</p>"
        f"<p>Usage:</p>"
        f"/api/v1.0/precipitation<br/>Returns a JSON list of percipitation data for the dates between 8/23/16 and 8/23/17<br/><br/>"
        f"/api/v1.0/stations<br/>Returns a JSON list of the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Returns a JSON list of the Temperature Observations (tobs) for each station for the dates between 8/23/16 and 8/23/17<br/><br/>"
        f"/api/v1.0/date<br/>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date and 8/23/17<br/><br/>."
        f"/api/v1.0/start_date/end_date<br/>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date and end date<br/><br/>."
    )


@app.route("/api/v1.0/precipitation")
def precipiation():
    # Date 12 months ago
    p_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= last_twelve_months).group_by(Measurement.date).all()
    return jsonify(p_results)

@app.route("/api/v1.0/stations")
def stations():
    s_results = session.query(Station.station, Station.name).all()
    return jsonify(s_results)

@app.route("/api/v1.0/tobs")
def tobs():
    t_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= last_twelve_months).all()
    return jsonify(t_results)   

@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(day_temp_results)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(multi_day_temp_results)

if __name__ == "__main__":
    app.run(debug=True)