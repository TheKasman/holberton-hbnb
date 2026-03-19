"""Repository code, currently switching from In-memory to SQLAlchemy"""

from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

class SQLAlchemyRepository(Repository):
    """Our new SQLAlchemy implementation"""
    def __init__(self, model):
        """constructor"""
        self.model = model

    def add (self, obj):
        """Adds something to the tables"""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Get a thing"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Get all the things"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an entry"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key): #  setting only attributes that exist
                    setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """Delete a thing"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Get by a certain attribute"""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
