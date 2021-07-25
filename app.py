from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from prediction import predict
import tempfile
import json
import pprint
import requests
import json


app = Flask(__name__)
app.logger.setLevel('INFO')
url='http://reg-4991.herokuapp.com/image'
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=FileStorage,
                    location='files',
                    required=True,
                    help='provide a file')

class Hello(Resource):

    def get(self):
        return {'word': '[tiger_cat,0.5858129858970642],[Egyptian_cat,0.210690438747406],'}



class Image(Resource):

    def post(self):
        args = parser.parse_args()
        the_file = args['file']
        # save a temporary copy of the file
        ofile, ofname = tempfile.mkstemp()
        the_file.save(ofname)

        return predict(ofname)




api.add_resource(Hello, '/hello')
api.add_resource(Image, '/image')

if __name__ == '__main__':
    app.run(debug=True)
