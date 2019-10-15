from flask_restful import Resource, reqparse, fields, marshal_with
from flask import request, jsonify, Response
from datetime import datetime

#from app.services import scraper_ubuntu
from app.models.target_image_model import TargetImageModel
from app.models.image_model import ImageModel


# Define schemas
image_fields = {
    'id': fields.Integer,
    'uuid': fields.String,
    'target_image_id': fields.String,
    'sha256': fields.String,
    'archive_path': fields.String,
    'image_format': fields.String,
    'source_url': fields.String,
    'build': fields.String,
    'datetime_created': fields.DateTime(dt_format='iso8601'),
    'datetime_modified': fields.DateTime(dt_format='iso8601'),
}


class Image(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        return jsonify({"message": "Not yet implemented!"})

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        image = ImageModel.query.get(args['id'])
        image.delete()
        result = dict()
        result['Message'] = {}
        result['Message'] = "Image deleted [id: {}, name: {}]".format(image.id, image.name)
        return jsonify({"message": "Not yet implemented!"})


class Images(Resource):
    @marshal_with(image_fields, envelope='image')
    def get(self):
        all_objects = ImageModel.get_all()
        return all_objects

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        return jsonify({"message": "Not yet implemented!"})
