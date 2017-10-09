# This server is designed to handle POST requests from google's API.AI
# from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import pywemo
from flask import Flask, request
from flask_restful import Api, Resource
import threading
from backend.wemo import wemo


class GenericRequest():
    def get_action_name(self):
        pass

    def handle_request(self, stuff):
        pass


class WemoRequest(GenericRequest):
    def get_action_name(self):
        return "wemo.change"

    def handle_request(self, parameters):
        light = parameters["light-location"]
        state = parameters["light-state"]
        getattr(wemo.WEMO_NAME_MAP[light], state)()
        print(
            "I was told to change {} and do {} to it".format(light, state))
        return {
            "displayText": "I changed the {} light!".format(light),
            "speech": "Changed your light."
        }


class Google(Resource):

    def __init__(self):
        self._requests = [WemoRequest()]


    def get(self):
        return "This webserver only handles POST requests", 200

    def post(self):
        json_data = request.json
        result = json_data["result"]
        parameters = result["parameters"]
        i = 0
        found = False
        while i < len(self._requests) and not found:
            if self._requests[i].get_action_name() == result["action"]:
                self._requests[i].handle_request(parameters)
                found = True
        if not found:
            return {"error": "invalidAction"}, 400


def build_listening_post():
    flask = Flask(__name__)
    api = Api(flask)
    api.add_resource(Google, "/")
    flask.run(host="0.0.0.0", port=8096)


def start_server():
    _thread = threading.Thread(name='daemon', target=build_listening_post)
    _thread.setDaemon(True)
    _thread.start()


if (__name__ == "__main__"):
    wemo.scan_for_devices()
    build_listening_post()
    # it just hates it
