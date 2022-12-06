import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

ORCID_CLIENT_ID = os.environ['ORCID_CLIENT_ID']
ORCID_CLIENT_SECRET = os.environ['ORCID_CLIENT_SECRET']

ORCID_SITE = os.environ.get('ORCID_SITE', "https://api.orcid.org")
ORCID_AUTHORIZE_URL = os.environ.get("ORCID_AUTHORIZE_URL", "https://orcid.org/oauth/authorize")
ORCID_TOKEN_URL = os.environ.get("ORCID_TOKEN_URL", "https://api.orcid.org/oauth/token")

