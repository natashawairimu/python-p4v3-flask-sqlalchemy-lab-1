# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)



# Routes
@app.route('/')
def index():
    return "<h1>Earthquake API</h1>"

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

#  New route for earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    quakes = [
        {
            "id": eq.id,
            "location": eq.location,
            "magnitude": eq.magnitude,
            "year": eq.year
        } for eq in earthquakes
    ]

    return jsonify({
        "count": len(quakes),
        "quakes": quakes
    }), 200
