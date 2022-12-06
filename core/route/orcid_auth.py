import logging

from flask import Blueprint
from flask import redirect, render_template, request, session, abort
import requests
import time
import logging as logger
from oauthlib.oauth2 import WebApplicationClient
from core import constants, utils, exceptions
from core.service import auth_service

auth = Blueprint('auth', __name__)
orcid = Blueprint('orcid', __name__)


@auth.route("/orcid")
def orcid_redirect():
    utils.set_host_url(request.host_url)
    client = WebApplicationClient(utils.get_app_config('ORCID_CLIENT_ID'))
    url = client.prepare_request_uri(utils.get_app_config('ORCID_AUTHORIZE_URL'),
                                     redirect_uri=utils.get_host_url() + constants.ORCID_REDIRECT_URL
                                                  + session[constants.USER_TOKEN_ID],
                                     scope="/authenticate /activities/update")
    return redirect(url)


@auth.route("/orcid/callback")
def orcid_callback():
    if 'code' in request.args:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'client_id=' + utils.get_app_config('ORCID_CLIENT_ID') + \
               '&client_secret=' + utils.get_app_config('ORCID_CLIENT_SECRET') + \
               '&grant_type=authorization_code&' \
               '&redirect_uri=' + utils.get_host_url() + constants.ORCID_REDIRECT_URL + request.args['token'] + \
               '&code=' + request.args["code"]

        response = requests.post(utils.get_app_config('ORCID_TOKEN_URL'), headers=headers, data=data, verify=False)
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

    else:
        logging.error("Error in the orcid call back " + request.json())
        abort(400)


@orcid.route("/claim")
def claim():
    status = None
    signed_in, orcid_info = utils.signed_in_info()

    if signed_in and 'doi' in request.args:
        doi = request.args['doi']

        if orcid_info:
            orcid_uid = orcid_info['orcid']
            access_token = orcid_info['access_token']

            headers = {
                'Accept': 'application/vnd.orcid+json',
                'Authorization': 'Bearer ' + access_token
            }

            response = requests.get("https://pub.sandbox.orcid.org/v3.0/0000-0002-6730-2500/works",
                                    headers=headers, verify=False)

            if response.status_code == 200:
                res_json = response.json()

                extracted_dois = []

                if 'group' in res_json:
                    works = res_json['group']

                    for work_loc in works:
                        if 'external-ids' in work_loc:
                            if 'external-id' in work_loc['external-ids']:
                                ids_loc = work_loc['external-ids']['external-id']
                                for id_loc in ids_loc:
                                    id_type = id_loc['external-id-type']
                                    id_val = id_loc['external-id-value']

                                    if id_type.upper() == 'DOI':
                                        extracted_dois.append(id_val)

                orcid_info['dois'] = extracted_dois

                url = constants.WORKS_API_URL + "/" + doi
                try:
                    res = requests.get(url)
                except Exception as e:
                    raise exceptions.APIConnectionException(e)

                if res.status_code == 200:
                    doi_record = None
                    response_json = res.json()
                    if response_json["message"]:
                        doi_record = response_json["message"]
                    if doi_record:
                        record = {
                            'title': doi_record['title'],

                        }
                        headers['Content-Type': 'application/vnd.orcid+json']
                        response = requests.post("https://pub.sandbox.orcid.org/v3.0/0000-0002-6730-2500/works",
                                                 data=doi_record, headers=headers, verify=False)
                        if response.status_code == 200:
                            pass

                    else:
                        status = 'no_such_doi'
                else:
                    status = 'no_such_doi'

            else:
                logger.error("API returns error. Status Code : " + response.status_code + " - Message : " +
                             response.text)

    return {"status": status}
