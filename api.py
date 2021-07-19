################################################################
#
# ZoomChatter - extract information from Zoom chat transcripts
# Copyright 2021 Peter Kaminski. Licensed under MIT License.
# https://github.com/keysandvalues/zoomchatter
#
################################################################

VERSION = 'v0.0.1'
APPNAME = 'ZoomChatter'

# Flask and Flask-RESTful
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

# get_links()
from urlextract import URLExtract

app = Flask(__name__)
api = Api(app)

def get_links(input):
    extractor = URLExtract()
    return extractor.find_urls(input)

class ZoomChatter(Resource):
    def post(self):
        # concatenate all uploaded files
        input = ''
        for key, file in request.files.items(multi=True):
            input += file.read().decode("utf-8")
        return {
            'length': len(input),
            'links': get_links(input),
        }

api.add_resource(ZoomChatter, '/zoomchatter')

if __name__ == '__main__':
    app.run(debug=True)
