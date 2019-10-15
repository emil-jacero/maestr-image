from app import ma
from app.models import TargetImageModel, ImageModel, ScheduleModel
from marshmallow import fields, Schema


class TargetImageSchema(Schema):
    id = fields.Integer(dump_only=True)  # Debug
    uuid = fields.String()
    os = fields.String()
    os_name = fields.String()
    os_version = fields.String()
    os_arch = fields.String()
    active = fields.Boolean()
    datetime_created = fields.DateTime()
    datetime_modified = fields.DateTime()


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)  # Debug
    uuid = fields.String()
    target_image = fields.Nested(TargetImageSchema)
    sha256 = fields.String()
    archive_path = fields.String()
    image_format = fields.String()
    source_url = fields.String()
    build = fields.String()
    datetime_created = fields.DateTime()
    datetime_modified = fields.DateTime()


class ScheduleSchema(Schema):
    id = fields.Integer(dump_only=True)  # Debug
    uuid = fields.String()
    name = fields.String()
    crontab = fields.String()
    target_images = fields.Nested(TargetImageSchema, many=True)
    datetime_created = fields.DateTime()
    datetime_modified = fields.DateTime()
