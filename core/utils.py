from flask import session
import uuid
import time
import core.constants as constants
from core.service import auth_service


CONFIG = None
BASE_ROOT = None
HOST_URL = None


def get_doi_url(doi):
    return "https://doi.org/"+doi


def signed_in_info():
    """
    Checks if the user is signed in and returns user info
    :return: True, user info if signed in else False and None. True if session expired
    """
    if constants.USER_TOKEN_ID in session:
        orcid_info = auth_service.get_orcid_info(session[constants.USER_TOKEN_ID])
        if orcid_info:
            time_now = time.time()
            if orcid_info['expires_at'] <= time_now:
                logout()
                # returns signed_in, orcid_info and expired
                return False, None, True
            else:
                return True, orcid_info, False

    else:
        session[constants.USER_TOKEN_ID] = str(uuid.uuid4())

    return False, None, False


def logout():
    if constants.USER_TOKEN_ID in session:
        auth_service.remove_user_info(session[constants.USER_TOKEN_ID])
        del session[constants.USER_TOKEN_ID]


def set_app_config(app_config):
    global CONFIG
    CONFIG = app_config


def get_app_config(key):
    if CONFIG:
        return CONFIG.get(key)
    return None


def set_base_path(app_root):
    global BASE_ROOT
    BASE_ROOT = app_root


def get_base_path():
    return BASE_ROOT


def set_host_url(host_url):
    global HOST_URL
    HOST_URL = host_url


def get_host_url():
    return HOST_URL
