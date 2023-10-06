#!/usr/bin/env python
import os

from flask import Flask, request, jsonify
from pymongo import MongoClient
from obstacles import getAllObstaclesOnTheWay, getAllObstacles
from get_directions import fetch_directions

app = Flask(__name__)

client = MongoClient("mongo:27017")

@app.route('/')
def todo():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"

@app.route('/directions', methods=['GET'])
def get_directions():
    # Default values for origin and destination
    # TODO: REMOVE once frontend input is possible
    default_origin = "BCG Düsseldorf"
    default_destination = "Curry, Hammer Str. 2, 40219 Düsseldorf"

    # Get origin and destination from query parameters or use defaults
    origin = request.args.get('origin', default_origin)
    destination = request.args.get('destination', default_destination)

    if not origin or not destination:
        return jsonify({'error': 'Origin and Destination are required'}), 400

    return fetch_directions(origin, destination)

# start and end parameters are coordinates in form "lat:lon"
@app.route('/obstacles', methods=['GET'])
def getObstacles():
    start = request.args.get('start', type=str)
    end = request.args.get('end', type=str)

    return jsonify({'obstacles': getAllObstaclesOnTheWay(start, end)})


if __name__ == "__main__":
    getAllObstacles()
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

