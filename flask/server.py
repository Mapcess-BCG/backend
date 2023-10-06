#!/usr/bin/env python
import os

from flask import Flask, request, jsonify
from pymongo import MongoClient

from bcg_to_currywurst_test import goEatCurryWurst
from integration import getAllRoutes
from obstacles import getAllObstacles, postObstacle
from polylines import get_polylines
from feedback import getFeedbackAlongTheRoute


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

@app.route('/feedback', methods=['GET'])
def getFeedback():
    return jsonify({'feedback': getFeedbackAlongTheRoute()})

@app.route('/feedback', methods=['POST'])
def postFeedback():
    data = request.get_json()
    postFeedback(data)
    print("Success")


@app.route('/routes', methods=['GET'])
def getRoute():
    origin = request.args.get('origin', type=str)
    destination = request.args.get('destination', type=str)
    return getAllRoutes(origin, destination)

@app.route('/obstacle', methods=['POST'])
def obstacle():
    return postObstacle(request.get_json())


if __name__ == "__main__":
    getAllObstacles()
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

