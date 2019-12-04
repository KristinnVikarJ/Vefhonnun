import os
import requests
from json import *
from time import *
from flask import Flask
from flask_cors import CORS
from threading import Thread

API_URL = "https://api.scpslgame.com/lobbylist.php?format=json"

TotalPlayers = 0
TotalCapacity = 0
TotalServers = 0
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    @app.route('/players')
    def players():
        return str(TotalPlayers)

    @app.route('/servers')
    def servers():
        return str(TotalServers)

    @app.route('/capacity')
    def capacity():
        return str(TotalCapacity)
    CORS(app)
    return app

def UpdateThread():
    global TotalPlayers
    global TotalCapacity
    global TotalServers
    while True:
        sleep(30)
        r = requests.get(API_URL)
        TotalPlayers = 0
        TotalCapacity = 0
        TotalServers = 0
        for jsonObject in r.json():
            TotalPlayers += int(jsonObject['players'].rsplit("/", 1)[0])
            TotalCapacity += int(jsonObject['players'].rsplit("/", 1)[-1])
            TotalServers += 1
        print("Total Players Playing: " + str(TotalPlayers))
        print("Total Servers Online: " + str(TotalServers))

thread = Thread(target = UpdateThread)
thread.start()