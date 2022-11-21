# URLs
BASE_API_URL = "http://api.crossref.org/"
WORKS_API_URL = BASE_API_URL + "works"
FUNDERS_API_URL = BASE_API_URL + "funders"
FUNDER_WORKS_API_URL = BASE_API_URL + "funders/{0}/works"
FUNDER_INFO_API_URL = BASE_API_URL + "funders/{0}"

# Categories
CATEGORY_HELP = "help"
CATEGORY_WORKS = "works"
CATEGORY_FUNDERS = "funders"
CATEGORY_REFERENCES = "references"

# Constant Values
ROWS_PER_PAGE = 20

MIN_MATCH_SCORE = 75
MIN_MATCH_TERMS = 3
MAX_MATCH_TEXTS = 1000

MESSAGE_TYPE_ERROR = "error"
MESSAGE_TYPE_INFO = "info"

# Exceptions
API_REQUEST_ERROR = "Could not able to connect to crossref API"
UNKNOW_ERROR = "Unknown error occurred "
