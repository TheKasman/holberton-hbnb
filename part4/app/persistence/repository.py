"""Repository layer (SQLAlchemy)"""

from abc import ABC, abstractmethod
from app.extensions import db


class Repository(ABC):
    """CRUD interface"""

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
    """Generic SQLAlchemy repository"""

    def __init__(self, model):
        """Set model"""
        self.model = model

    def add(self, obj):
        """Add object"""
        from app import db
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Get by id"""
        return db.session.get(self.model, obj_id)

    def get_all(self):
        """Get all"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update fields"""
        from app import db
        obj = self.get(obj_id)
        if not obj:
            return None

        ignore_fields = {"id", "created_at"}

        for key, value in data.items():
            if key in ignore_fields:
                continue

            setter_method = f"set_{key}"
            if hasattr(obj, setter_method):
                getattr(obj, setter_method)(value)
            elif hasattr(obj, key):
                setattr(obj, key, value)

        db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete by id"""
        from app import db
        obj = self.get(obj_id)
        if not obj:
            return None

        db.session.delete(obj)
        db.session.commit()
        return obj

    def get_by_attribute(self, attr_name, attr_value):
        """Get by attribute"""
        return self.model.query.filter_by(
            **{attr_name: attr_value}
        ).first()