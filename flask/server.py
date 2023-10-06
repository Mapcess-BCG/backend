#!/usr/bin/env python
import os

from flask import Flask, request, jsonify
from pymongo import MongoClient

from bcg_to_currywurst_test import goEatCurryWurst
from obstacles import getAllObstaclesOnTheWay, getAllObstacles
from polylines import get_polylines

app = Flask(__name__)

client = MongoClient("mongo:27017")

@app.route('/')
def todo():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"

# returns a list of polylines
@app.route('/directions', methods=['GET'])
def get_directions():
    # Get origin and destination from query parameters or use defaults
    origin = request.args.get('origin', type=str)
    destination = request.args.get('destination', type=str)

    return get_polylines(origin, destination)

# start and end parameters are coordinates in form "lat:lon"
@app.route('/obstacles', methods=['GET'])
def getObstacles():
    start = request.args.get('start', type=str)
    end = request.args.get('end', type=str)

    return jsonify({'obstacles': getAllObstaclesOnTheWay(start, end)})


@app.route('/test', methods=['GET'])
def runTest():
    goEatCurryWurst()
    return jsonify({'output': "worked"})


if __name__ == "__main__":
    getAllObstacles()
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

