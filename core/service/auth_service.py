ORCID_SESSION = {}


def set_orcid_info(token, orcid_info):
    global ORCID_SESSION
    ORCID_SESSION[token] = orcid_info


def get_orcid_info(token):
    if token in ORCID_SESSION:
        return ORCID_SESSION[token]
    else:
        return None
