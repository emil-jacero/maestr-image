# -*- coding:utf-8 -*-
from flask import abort
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app import db


class IdMixin(object):
    """
    Provides the :attr:`id` primary key column
    """
    #: Database identity for this model, used for foreign key
    #: references from other models
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=lambda: str(uuid4()))


class NameMixin(object):
    """
    Provides the :attr:`name` and `slug`
    """
    #: Full name
    name = db.Column(db.String(200), nullable=False, index=True)
    #: Name made friendly for urls
    slug = db.Column(db.String(200), nullable=False)


class TimestampMixin(object):
    """
    Provides the :attr:`datetime_created`, :attr:`datetime_modified` and  audit timestamps
    """
    #: Timestamp for when this instance was created, in UTC
    datetime_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    #: Timestamp for when this instance was last updated (via the app), in UTC
    datetime_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    #: Timestamp for when this instance was deleted. Use with CRUDMixin
    datetime_deleted = db.Column(db.DateTime, nullable=True)


class CustomerMixin(object):
    """
    Provides the :attr:`customer_name` and :attr:`customer_orgnr`
    """
    #:
    customer_name = db.Column(db.String(100), nullable=False)
    #:
    customer_orgnr = db.Column(db.Integer, unique=True, nullable=False)


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    deleted = db.Column(db.Boolean, default=False, nullable=False)
    db.Index('idx_deleted', deleted)

    @classmethod
    def query(cls):
        return db.session.query(cls)

    @classmethod
    def get(cls, _id):
        if any((isinstance(_id, basestring) and _id.isdigit(),
                isinstance(_id, (int, float))), ):
            return cls.query.get(int(_id))
        return None

    @classmethod
    def get_or_404(cls, _id):
        rv = cls.get(_id)
        if rv is None:
            abort(404)
        return rv

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def get_or_create(cls, **kwargs):
        r = cls.get_by(**kwargs)
        if not r:
            r = cls(**kwargs)
            db.session.add(r)
        return r

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        return self

    def delete(self, commit=True):
        self.deleted = True
        self.datetime_deleted = datetime.utcnow()
        self.datetime_modified = self.datetime_deleted
        return commit and db.session.commit()