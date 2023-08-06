import requests
import json
from typing import Dict
from .tegro_config import TegroConfig
from .build_dict import build_dict
from .build_headers import build_headers


def post(config: TegroConfig, endpoint: str, body: Dict = None) -> Dict:
    api_url, shop_id, api_key = set(config.dict().values())
    url = api_url + endpoint
    body = build_dict(shop_id, body)
    headers = build_headers(api_key, body)
    try:
        response = requests.post(url, data=body, headers=headers)
        response.raise_for_status()
        response_text = json.loads(response.text)
        return response_text
    except Exception as e:
        print(e)
        return None