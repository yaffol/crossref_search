from models.model import OrcidUser
from core.database import db


def set_orcid_info(token, orcid_info):
    """
    Add or update orcid user info in database
    :param token: session token
    :param orcid_info: orcid info to save
    :return:
    """
    user = OrcidUser.query.filter_by(orcid_id=orcid_info['orcid']).first()
    if user:
        user.session_token = token
        user.orcid_info = orcid_info
        db.session.add(user)
        db.session.commit()
    else:
        new_user = OrcidUser(session_token=token, orcid_id = orcid_info['orcid'], orcid_info = orcid_info)
        db.session.add(new_user)
        db.session.commit()


def get_orcid_info(token):
    """
    Get the Orcid profile information
    :param token: session token
    :return: orcid info
    """
    user = OrcidUser.query.filter_by(session_token=token).first()
    if user:
        return user.orcid_info
    else:
        return None
