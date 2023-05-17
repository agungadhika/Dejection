import requests
from .parse import postParser
# from parse import postParser
from requests.utils import requote_uri
from bs4 import BeautifulSoup as bs4
import re


def createSession(url):
    s = requests.Session()
    soup = bs(s.get(url).content, "html.parser")
    hidden = soup.find("input", type="hidden")
    token = hidden.get("value")
    payload = {"username": "admin", "password": "password", "Login":"Login", "user_token": token}
    s.post(url, data=payload)
    return s

def findInput(url):
    # s = createSession(URL)
    # content = s.get(url).content
    content = requests.get(url).content
    soup = bs4(content, "html.parser")
    input_form = soup.find_all("input")
    return [i.get("name") for i in input_form if i.get("name") is not None]

def post_validation(url: str, type_attack: str):
    context_data = {}
    input_id = findInput(url) # type list
    context_data = {
        "url": url,
        "input_id": input_id,
        "type_attack": type_attack
    }
    return context_data

# post request -> url, payloads, data (x-urlformencoded)

def post_request(url: str, payloads: list, data: dict):
    # get each value from data.values()
    # from value, check whether it has "$$" or not
    #   if "$$" exists, change to payload
    #   else, continue to another value
    # return data dictionary filled with payloads

    # initial_data = {"ie": "", "gl": "$$"}

    # data = [{"ie": payload1, "hl": "a", "h3": "b"}, {"ie": payload2, "hl": "a", "h3": "b"}]
    # requests.post(url, data=data)
    current_data = data.copy()
    for key, value in data.items():
        if (re.search("\$(.*?)\$", value) != None):
            v = postParser(value, payloads)
            current_data[key] = v
    
    processed_data = []
    for key, value in current_data.items():
        if (len(value) > 1):
            for item in value:
                initial_data = data.copy()
                initial_data[key] = item
                processed_data.append(initial_data) # not a copy?
    
    result = []
    for index, value_dict in enumerate(processed_data):
        response = requests.post(url, json = value_dict)
        status_code = response.status_code
        try:
            content_length = response.headers["Content-Length"]
        except:
            content_length = len(response.text)
        result.append([payloads[index], status_code, content_length]) 
    return result

# print(post_request("http://gaggle.com", ["good payload", "great payload", "wonderful payload"], {"ie": "$$", "hl": "a", "h3": "b"}))