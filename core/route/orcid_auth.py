from flask import Blueprint
from flask import redirect, render_template, request, session, abort
import requests
import time
import logging as logger
from oauthlib.oauth2 import WebApplicationClient
from core import constants, utils
from core.service import auth_service

auth = Blueprint('auth', __name__)


@auth.route("/orcid")
def orcid():
    client = WebApplicationClient(utils.get_app_config('ORCID_CLIENT_ID'))
    url = client.prepare_request_uri(constants.ORCID_AUTHORIZE_URL,
                                     redirect_uri=constants.ORCID_REDIRECT_URL + session[constants.USER_TOKEN_ID],
                                     scope="/authenticate")
    return redirect(url)


@auth.route("/orcid/callback")
def orcid_callback():
    if 'code' in request.args:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'client_id='+utils.get_app_config('ORCID_CLIENT_ID') +\
               '&client_secret='+utils.get_app_config('ORCID_CLIENT_SECRET') +\
               '&grant_type=authorization_code&' \
               '&redirect_uri=' + constants.ORCID_REDIRECT_URL + request.args['token'] +\
               '&code=' + request.args["code"]

        response = requests.post(constants.ORCID_TOKEN_URL, headers=headers, data=data, verify=False)
        if response.status_code == 200:

            res_json = response.json()
            res_json['expires_at'] = int(time.time()) + res_json['expires_in']

            if 'token' in request.args:
                session_token = request.args['token']
                auth_service.set_orcid_info(session_token, res_json)

            return render_template("auth_callback.html")
        else:
            logger.error("Error in orcid authorization response: status code: " +
                         str(response.status_code) + ' message: ' + response.text)
            abort(400)
