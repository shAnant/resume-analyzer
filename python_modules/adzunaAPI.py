

from requests import Response,get
import pandas as pd
import numpy as np
import json
import os
from dotenv import load_dotenv

load_dotenv()

ADZUNA_API = os.getenv('ADZUNA_API')
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID')
ADZUNA_url = os.getenv('ADZUNA_url')


params = {
    "app_id" : ADZUNA_APP_ID,
    "app_key" : ADZUNA_API, 
    "what" : "Machine Learning",
    "where" : "Noida"
}

response = get(url=ADZUNA_url, params=params).json()

print(json.dumps(response, indent=2))
