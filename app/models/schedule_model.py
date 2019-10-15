from app import db
from app.models.mixin import IdMixin, TimestampMixin, CRUDMixin
from app.models import TargetImageModel

target_images = db.Table('target_images_schedules',
                db.Column('target_image_id', db.Integer, db.ForeignKey('target_image.id', ondelete='cascade')),
                db.Column('schedule_id', db.Integer, db.ForeignKey('schedule.id', ondelete='cascade'))
)


class ScheduleModel(db.Model, IdMixin, TimestampMixin, CRUDMixin):
    __tablename__ = 'schedule'

    name = db.Column(db.String(200), nullable=False)  # Display name
    crontab = db.Column(db.String(200), nullable=False)  # crontab based on unix
    target_image = db.relationship('TargetImageModel', secondary=target_images, backref=db.backref('schedule'),
                                 lazy='select')

    def __init__(self, data):
        self.uuid = data.get('uuid')
        self.name = data.get('name')
        self.crontab = data.get('crontab')
        self.datetime_created = data.get('datetime_created')
        self.datetime_modified = data.get('datetime_modified')

    @staticmethod
    def get_all():
        return ScheduleModel.query.all()

    @staticmethod
    def get_one():
        return ScheduleModel.query.get(id)

    @staticmethod
    def get_one_by_uuid(uuid, deleted=False):
        return ScheduleModel.query.filter_by(uuid=uuid, deleted=deleted).first()

    def __repr(self):
        return '<id {}>'.format(self.id)
