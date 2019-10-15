from app import db
from app.models.mixin import IdMixin, TimestampMixin, CRUDMixin


class TargetImageModel(db.Model, IdMixin, TimestampMixin, CRUDMixin):
    __tablename__ = 'target_image'

    os = db.Column(db.String(200), nullable=False)  # Windows or Linux
    os_name = db.Column(db.String(200), nullable=False)  # Given name (ex. Ubuntu)
    os_version = db.Column(db.String(200), nullable=False)  # OS Version (ex. 18.04)
    os_arch = db.Column(db.String(200), nullable=False)  # OS Architecture (ex. x86_64, arm)
    active = db.Column(db.Boolean, nullable=False)  # Should the image be on the schedule

    def __init__(self, data):
        self.uuid = data.get('uuid')
        self.os = data.get('os')
        self.os_name = data.get('os_name')
        self.os_version = data.get('os_version')
        self.os_arch = data.get('os_arch')
        self.active = data.get('active')
        self.datetime_created = data.get('datetime_created')
        self.datetime_modified = data.get('datetime_modified')

    @staticmethod
    def get_all():
        return TargetImageModel.query.all()

    @staticmethod
    def get_one():
        return TargetImageModel.query.get(id)

    def __repr(self):
        return '<id {}>'.format(self.id)