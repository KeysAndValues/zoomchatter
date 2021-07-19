################################################################
#
# ZoomChatter - extract information from Zoom chat transcripts
# Copyright 2021 Peter Kaminski. Licensed under MIT License.
# https://github.com/keysandvalues/zoomchatter
#
################################################################

VERSION = 'v0.0.1'
APPNAME = 'ZoomChatter'

import re

# Flask and Flask-RESTful
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

# get_links()
from urlextract import URLExtract

app = Flask(__name__)
api = Api(app)

# links
# participants
# clean
# clean_grouped
# clean_no_names

# ?output=
# ?flags=include_private
# ?format=html (text (utf-8), ascii, markdown, HTML, JSON)

def get_participants(input):
    participants = re.findall(r"^\d\d:\d\d:\d\d\t([^\t]+):\t", input, re.MULTILINE)
    return list(set(participants))

def get_links(input):
    extractor = URLExtract()
    urls = extractor.find_urls(input)
    return list(set(urls))

def get_clean(input):
    names_and_lines = re.findall(r"^\d\d:\d\d:\d\d\t([^\t]+):\t([^\n\r]*)", input, re.MULTILINE)
    return names_and_lines

def get_clean_no_names(input):
    lines = re.findall(r"^\d\d:\d\d:\d\d\t[^\t]+:\t([^\n\r]*)", input, re.MULTILINE)
    return "\n\n".join(lines)

def get_lines(input):
    return input.splitlines()

class ZoomChatter(Resource):
    def post(self):
        # concatenate all uploaded files
        input = ''
        for key, file in request.files.items(multi=True):
            input += file.read().decode("utf-8")
        # change different possible linebreak characters to \n
        re.sub(r"[\n\r]|\u2028", "\n", input)

        # return data
        return {
            'input_length': len(input),
            'participants': get_participants(input),
            'links': get_links(input),
#            'clean': get_clean(input),
#            'clean_no_names': get_clean_no_names(input),
            'lines': get_lines(input),
            'input_linebreaks_fixed': input,
        }

api.add_resource(ZoomChatter, '/zoomchatter')

if __name__ == '__main__':
    app.run(debug=True)
