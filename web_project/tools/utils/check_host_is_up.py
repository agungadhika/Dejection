import requests
from urllib.parse import urlparse
def is_host_up(host: str) -> bool:
    try:
        protocol = urlparse(host).scheme
        domain = urlparse(host).netloc
        request_result = requests.head(f"{protocol}://{domain}", timeout=10)
    except requests.ConnectionError:
        print("request connection error")
        return False
    if (request_result.status_code not in [200, 302, 301]):
        print("status code is not correct", request_result.status_code)
        return False
    return True

"""

{"username": "value", "password": "value"}
{, "password": "value"}
{{}, "password": "value"}

"""