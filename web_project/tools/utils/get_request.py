from .parse import parser
from requests.utils import requote_uri
import requests
from .check_host_is_up import is_host_up
# payloads is common across all attack type, therefore we can simplify this by 
# giving payloads as argument


def get_request(url: str, payloads: list):
    if (not is_host_up(url)):
        raise requests.ConnectionError("Host is Down")
    parsed_text = parser(url, payloads)
    url_payload = list(map(requote_uri, parsed_text["url_payload"]))
    result = []
    for index, url in enumerate(url_payload):
        response = requests.get(url)
        status_code = response.status_code
        try:
            content_length = response.headers["Content-Length"]
        except:
            content_length = len(response.text)
        result.append([payloads[index], status_code, content_length])
    return result