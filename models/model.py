from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from core.database import db


class OrcidUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String())
    orcid_id = db.Column(db.String())
    orcid_info = db.Column(JSON)
