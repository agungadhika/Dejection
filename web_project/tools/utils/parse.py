# get url
# parse using regular expression
# check for colon (:), if exists, the last portion of host is port
# return results
import re
def parser(url: str, payloads: list):
    text_list = []
    port = None
    if "http" not in url:
        url = "http://" + url
    for payload in payloads:
        text_list.append(re.sub("\$(.*?)\$", payload, url))
    return {"url_payload": text_list}

def postParser(data: str, payloads: list):
    text_list = []
    for payload in payloads:
        text_list.append(re.sub("\$(.*?)\$", payload, data))
    return text_list