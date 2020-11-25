import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("postgresql://postgres:Gamecock2020!@localhost:5432/sqlalchemy-challenge")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurements
Station = Base.classes.stations

app = Flask(__name__)
session = Session(engine)

last12months = session.query(Measurement.date).order_by(Measurement.date.desc()).all()
last_data_point = dt.date(2017, 8, 23) - dt.timedelta(days=365)
MostActive = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281')

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()
        
    session.close()
    
    precipitation = []
    for result in results:
        r = {}
        r[result[0]] = result[1]
        precipitation.append(r)

    return jsonify(precipitation )


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016, 8, 18').all()
    return jsonify(results)


@app.route("/api/v1.0/<start>")
def start(start):
    start = dt.date(2016, 8, 18)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def start(start):
    start = dt.date(2016, 8, 18)
    end = dt.date(2017, 8, 18)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results)