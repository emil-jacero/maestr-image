from flask_restful import Resource, reqparse, fields, marshal_with
from flask import request, jsonify, Response
from datetime import datetime
from app.services.helpers import ImageObject

from app.models.target_image_model import TargetImageModel
from app.models.image_model import ImageModel
from app.models import ScheduleModel


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

schedule_fields = {
    'id': fields.Integer,
    'uuid': fields.String,
    'name': fields.String,
    'crontab': fields.String,
    'target_image': fields.List(fields.Nested(target_image_fields)),
    'datetime_created': fields.DateTime(dt_format='iso8601'),
    'datetime_modified': fields.DateTime(dt_format='iso8601'),
}


class Schedule(Resource):
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


class Schedules(Resource):
    @marshal_with(schedule_fields, envelope='scheduler')
    def get(self):
        all_objects = ScheduleModel.get_all()
        return all_objects

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        return jsonify({"message": "Not yet implemented!"})


class RunManually(Resource):
    def post(self, uuid):
        schedule = ScheduleModel.get_one_by_uuid(uuid)
        all_target_images = schedule.target_image

        for image in all_target_images:
            test = ImageObject(image.os_name, image.os_version)
            test.find_latest_build(os_arch=image.os_arch)
            print(test.os_name, test.os_version, test.sha256, test.source_url, test.build, test.archive_path, test.image_format)

        return fields.marshal(all_target_images, target_image_fields, envelope='target_image')
