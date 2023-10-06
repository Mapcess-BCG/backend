#!/usr/bin/env python
import os

from flask import Flask, request, jsonify
from pymongo import MongoClient

from obstacles import getAllObstaclesOnTheWay, getAllObstacles

app = Flask(__name__)

client = MongoClient("mongo:27017")

@app.route('/')
def todo():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"


# start and end parameters are coordinates in form "lat:lon"
@app.route('/obstacles', methods=['GET'])
def getObstacles():
    start = request.args.get('start', type=str)
    end = request.args.get('end', type=str)

    return jsonify({'obstacles': getAllObstaclesOnTheWay(start, end)})






if __name__ == "__main__":
    getAllObstacles()
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
