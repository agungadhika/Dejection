# get url
# parse using regular expression
# check for colon (:), if exists, the last portion of host is port
# return results
import re
from urllib.parse import quote_plus
from typing import List
def parser(url: str, payloads: list):
    text_list = []
    port = None
    if "http" not in url:
        url = "http://" + url
    for payload in payloads:
        text_list.append(re.sub("\$(.*?)\$", quote_plus(payload), url))
    return {"url_payload": text_list}

def postParser(data: str, payloads: list) -> List[str]:
    text_list = []
    for payload in payloads:
        text_list.append(re.sub("\$(.*?)\$", payload, data))
    return text_list