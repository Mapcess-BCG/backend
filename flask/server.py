#!/usr/bin/env python
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from bcg_to_currywurst_test import goEatCurryWurst
from integration import getAllRoutes
from obstacles import getAllObstacles, postObstacle, getObstacleImg
from polylines import get_polylines
from feedback import getFeedbackAlongTheRoute, postFeedback

app = Flask(__name__)
CORS(app)

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

# we get feedback with route
@app.route('/feedback', methods=['GET'])
def getFeedback():
    return jsonify({'feedback': getFeedbackAlongTheRoute()})

@app.route('/feedback', methods=['POST'])
def feedback():
    return postFeedback(request.get_json())


@app.route('/routes', methods=['GET'])
def getRoute():
    origin = request.args.get('origin', type=str)
    destination = request.args.get('destination', type=str)
    return getAllRoutes(origin, destination)

@app.route('/obstacle', methods=['POST'])
def obstacle():
    return postObstacle(request.get_json())


@app.route('/img', methods=['GET'])
def getImgs():
    return getObstacleImg()


if __name__ == "__main__":
    getAllObstacles()
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

