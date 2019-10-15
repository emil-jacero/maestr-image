from flask_restful import Resource, reqparse, fields, marshal_with
from flask import request, jsonify, Response
from datetime import datetime

#from app.services import scraper_ubuntu
from app.models.target_image_model import TargetImageModel
from app.models.image_model import ImageModel


# Define schemas
target_image_fields = {
    'id': fields.Integer,
    'uuid': fields.String,
    'os': fields.String,
    'os_name': fields.String,
    'os_version': fields.String,
    'os_arch': fields.String,
    'active': fields.Boolean,
    'datetime_created': fields.DateTime(dt_format='iso8601'),
    'datetime_modified': fields.DateTime(dt_format='iso8601'),
}


class TargetImage(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        return jsonify({"message": "Not yet implemented!"})

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        return jsonify({"message": "Not yet implemented!"})

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        return jsonify({"message": "Not yet implemented!"})


class TargetImages(Resource):
    @marshal_with(target_image_fields, envelope='target_image')
    def get(self):
        all_objects = TargetImageModel.get_all()
        return all_objects

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        return jsonify({"message": "Not yet implemented!"})