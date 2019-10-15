from app import db
from app.models.mixin import IdMixin, TimestampMixin, CRUDMixin
from app.models.target_image_model import TargetImageModel


class ImageModel(db.Model, IdMixin, TimestampMixin, CRUDMixin):
    __tablename__ = 'image'

    target_image_id = db.Column(db.Integer, db.ForeignKey('target_image.id'), nullable=False)
    sha256 = db.Column(db.String(200), nullable=False, unique=True)  # Hash from publisher
    archive_path = db.Column(db.String(200), nullable=True)  # URL or local path to downloaded image
    image_format = db.Column(db.String(40), nullable=True)  # RAW, QCOW2, etc.
    source_url = db.Column(db.String(200), nullable=False)  # URL where the image was downloaded from
    build = db.Column(db.String(40), nullable=False)  # OS Build (1907)

    image = db.relationship('TargetImageModel', backref='image')

    def __init__(self, data):
        self.uuid = data.get('uuid')
        self.target_image_id = data.get('target_image_id')
        self.sha256 = data.get('sha256')
        self.archive_path = data.get('archive_path')
        self.format = data.get('format')
        self.source_url = data.get('source_url')
        self.build = data.get('os_build')
        self.datetime_created = data.get('datetime_created')
        self.datetime_modified = data.get('datetime_modified')

    @staticmethod
    def get_all():
        return ImageModel.query.all()

    @staticmethod
    def get_one():
        return ImageModel.query.get(id)

    @staticmethod
    def image_exists(image_sha256):
        exists = db.session.query(db.exists().where(ImageModel.sha256 == image_sha256)).scalar()
        return exists

    def __repr(self):
        return '<id {}>'.format(self.id)