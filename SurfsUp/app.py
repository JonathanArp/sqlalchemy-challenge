import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
import datetime as dt

#database connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
base = automap_base()
base.prepare(autoload_with=engine)
print(base.classes.keys())
#references to tables
measurement = base.classes.measurement
station = base.classes.station

#Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def home():
    return (f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>didnotcomplete<br/>"
        f"/api/v1.0/<start>/<end>didnotcomplete"
        )

@app.route("/api/v1.0/precipitation")
def prec():
    session = Session(engine)
    previous_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_date).all()
    session.close()
    empty_list = []
    for date, prcp in results:
        list_dict = {}
        list_dict["date"] = date
        list_dict["prcp"] = prcp
        empty_list.append(list_dict)
    return jsonify(empty_list)

@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    return jsonify(list(np.ravel(results)))

@app.route("/api/v1.0/tobs")
def tob():
    session = Session(engine)
    previous_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == "USC00519281").\
        filter(measurement.date >= previous_date).all()
    session.close()
    results = list(np.ravel(results))
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start():
    return (f"Howdy!")

@app.route("/api/v1.0/<start>/<end>")
def end():
    return (f"Howdy!")

if __name__ == "__main__":
    app.run(debug=True)