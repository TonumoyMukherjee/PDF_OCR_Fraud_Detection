# -*- coding: utf-8 -*-
"""
Created on Fri May 20 16:36:29 2022

@author: tonumoy
"""

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

videos = {}

class video (Resource):
    def get(self, video_id):
          return videos[video_id]

    
    
api.add_resource(HelloWorld, "/helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)