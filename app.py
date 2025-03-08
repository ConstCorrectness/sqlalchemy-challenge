from flask import Flask, jsonify, render_template
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pathlib

db_path = pathlib.Path('Resources/hawaii.sqlite')


# Database Setup
engine = create_engine(f'sqlite:///{db_path}')

Base = automap_base()
Base.prepare(engine, reflect=True)

# ORM-Classes (tables in our .sqlite)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)         # Session = sessionmaker(engine); session = Session()??



# Create an app, being sure to pass __name__
app = Flask(__name__)

# Use Flask to create your routes as follows:
# /
# Home page.
# List all routes that are available.

@app.route("/")
def home():
    return render_template('index.html')

# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Query for the dates and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precipitation = []
    for res in results:
        precipitation_dict = {}
        precipitation_dict[res[0]] = res[1]
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query for stations
    results = session.query(Station.station).all()

    session.close()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Query for the dates/temps at the most active station
    most_active_station = 'USC00519281'
    most_active_station_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).all()

    session.close()

    all_tobs = []
    for date, tobs in most_active_station_data:
        tobs_dict = {}
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

# /api/v1.0/<start>
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Start' page...")
    session = Session(engine)

    # Query for the min, avg, max temps for date >= start
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    all_start_temps = list(np.ravel(results))

    return jsonify(all_start_temps)

# /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")

def start_end(start, end):
    print("Server received request for 'Start-End' page...")
    session = Session(engine)

    # i like select() better than query(), but mehs
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    all_start_end_temps = list(np.ravel(results))

    return jsonify(all_start_end_temps)

if __name__ == "__main__":
    app.run(debug=True)


