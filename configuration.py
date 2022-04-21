import os
from constants import *

ENVIRONMENT = os.environ.get(ENVIRONMENT_KEY, TEST_ENVIRONMENT_KEY)
if ENVIRONMENT == TEST_ENVIRONMENT_KEY:
    from dotenv import load_dotenv
    load_dotenv()

ACCOUNT_SID = os.environ.get(ACCOUNT_SID_KEY)
AUTH_TOKEN = os.environ.get(AUTH_TOKEN_KEY)
OPENAI_API_TOKEN = os.getenv(OPENAI_API_KEY)
