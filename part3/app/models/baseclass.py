from app import db
import uuid
from datetime import datetime, timezone


class BaseModel(db.Model):
    """
    Abstract base class for all database models.

    This class provides:
    - A UUID primary key (`id`)
    - Automatic timestamping (`created_at`, `updated_at`)
    - Common persistence methods (`save`, `update`)

    NOTE:
    __abstract__ = True prevents SQLAlchemy from creating a table
    for this class. It is meant to be inherited by other models.
    """
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Use timezone-aware datetime (recommended over deprecated utcnow())
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def save(self):
        """
        Persist the current object to the database.

        This method:
        - Updates the `updated_at` timestamp using timezone-aware UTC time
        - Adds the object to the current database session
        - Commits the transaction

        Note:
        We use `datetime.now(timezone.utc)` instead of `datetime.utcnow()`
        because `utcnow()` is deprecated and returns a naive datetime.
        """
        self.updated_at = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """
        Update the object's attributes using a dictionary.

        Args:
            data (dict): Dictionary of attributes to update.

        Behavior:
        - Ignores protected fields such as 'id' and 'created_at'
        - Updates only attributes that exist on the model
        - Automatically saves changes to the database

        """
        ignore_fields = {"id", "created_at"}

        for key, value in data.items():
            if key in ignore_fields:
                continue

            if hasattr(self, key):
                setattr(self, key, value)

        self.save()