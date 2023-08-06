import os
from typing import Dict

def get_apis_from_env() -> Dict[str, str]:
    search_strings = ['_API_KEY', '_SECRET_KEY', '_SUBSCRIPTION_KEY']

    api_keys = {}

    for key, value in os.environ.items():
        for search_string in search_strings:
            if search_string in key:
                name = key.split(search_string)[0].lower().replace("_", "-")
                api_keys[name] = value

    return api_keys