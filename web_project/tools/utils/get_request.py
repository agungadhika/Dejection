from .parse import parser
from requests.utils import requote_uri
import requests

# payloads is common across all attack type, therefore we can simplify this by 
# giving payloads as argument

def get_request(url: str, payloads: list):
    parsed_text = parser(url, payloads)
    url_payload = map(requote_uri, parsed_text["url_payload"])
    result = []
    for index, url in enumerate(url_payload):
        response = requests.get(url)
        status_code = response.status_code
        content_length = response.headers["Content-Length"]
        result.append([payloads[index], status_code, content_length])
    return result