# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import os
import datetime as dt 

#################################################
# Database Setup
#################################################
os.chdir(os.path.dirname(os.path.realpath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurments = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def avalible_routes():
    html = """Avalible Routes:<br>
            /api/v1.0/precipitation<br>
            /api/v1.0/stations<br>
            /api/v1.0/tobs<br>
            /api/v1.0/tstats/&lt;start&gt;<br>
            /api/v1.0/tstats/&lt;start&gt;/&lt;end&gt;<br>"""
    return html  


@app.route("/api/v1.0/precipitation/")
def percipitation():
    session = Session(engine)
    last_date_str = session.query(Measurments.date).order_by(Measurments.date.desc()).limit(1).scalar()
    last_date = dt.date.fromisoformat(last_date_str)
    year_before_last = last_date - dt.timedelta(days=365)

    precipiation_results = session.query(Measurments.date, func.avg(Measurments.prcp).label("prcp"))\
     .filter(Measurments.date >= year_before_last)\
     .group_by(Measurments.date)\
     .order_by(Measurments.date)\
     .all()
    session.close()
    results =  [dict(row) for row in precipiation_results]
    print(results)
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)


@app.route("/api/v1.0/tstats/<start>/")
@app.route("/api/v1.0/tstats/<start>/<end>/")
def tstats(start, end=dt.date(dt.MAXYEAR, 12, 31)):
    return jsonify([start, end])


if __name__ == '__main__':
    app.run(debug=True)