import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

ORCID_CLIENT_ID = os.environ['ORCID_CLIENT_ID']
ORCID_CLIENT_SECRET = os.environ['ORCID_CLIENT_SECRET']

