from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from core.database import db


class OrcidUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String())
    orcid_id = db.Column(db.String())
    orcid_info = db.Column(JSON)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
