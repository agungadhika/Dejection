# from requests.utils import requote_uri
from urllib.parse import urlparse, quote
import requests
from .parse import parser
from .check_host_is_up import is_host_up
from .post_request import createSessionBwapp, URL
# from parse import parser
# from check_host_is_up import is_host_up
# from post_request import createSessionBwapp, URL


# payloads are common across all attack type, therefore we can simplify this by 
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
    url_payload = parsed_text["url_payload"]
    result = []
    for index, url in enumerate(url_payload):
        response = session.get(url)
        status_code = response.status_code
        try:
            content_length = response.headers["Content-Length"]
        except Exception as e:
            print(e)
            content_length = len(response.text)
        result.append([payloads[index], status_code, content_length])
    return result

# unit testing passed
if __name__ == "__main__":
    payloads=['OR 1=1',
            '<form><a href="javascript:\u0061lert&#x28;1&#x29;">CLICK']
    result = get_request("https://bwapp.hakhub.net/xss_get.php?firstname=mynameiskrisna$$&lastname=asdf&form=submit", payloads=payloads, login_dvwa=True)
    print(result)