import requests
from .parse import postParser
# from parse import postParser
# from ..models import xss
# from requests.utils import requote_uri
from urllib.parse import quote as requote_uri
from bs4 import BeautifulSoup as bs4
import re


URL = "https://bwapp.hakhub.net/login.php"

def createSessionDvwa(url, username="admin", password="password"):
    s = requests.Session()
    soup = bs4(s.get(url).content, "html.parser")
    hidden = soup.find("input", type="hidden")
    token = hidden.get("value")
    payload = {"username": username, "password": password, "Login":"Login", "user_token": token}
    s.post(url, data=payload)
    return s

def createSessionBwapp(url, username="ikantongkol", password="hacker", security_level=0):
    s = requests.Session()
    payload = {"login": username, "password": password, "security_level":security_level, "form": "submit"}
    s.post(url, data=payload)
    return s

def findInput(url, session = None):
    # s = createSessionBwapp(URL)
    # content = s.get(url).content
    if (session is not None):
        content = session.get(url).content
    else:
        content = requests.get(url).content
    soup = bs4(content, "html.parser")
    input_form = soup.find_all("input")
    return [i.get("name") for i in input_form if i.get("name") is not None]

def findSelect(url, session = None):
    if (session is not None): 
        content = session.get(url).content
    else:
        content = requests.get(url).content
    soup = bs4(content, "html.parser")
    select_form = soup.find_all("select")
    return [i.get("name") for i in select_form if i.get("name") is not None]

def post_validation(url: str, type_attack: str, login_dvwa: bool = False):
    context_data = {}
    if (login_dvwa):
        session = createSessionBwapp(URL)
        input_id = findInput(url, session)
        input_id += findSelect(url, session)
    else:
        input_id = findInput(url) # type list
        input_id += findSelect(url)
    
    context_data = {
        "url": url,
        "input_id": input_id,
        "type_attack": type_attack
    }
    return context_data

# post request -> url, payloads, data (x-urlformencoded)

def post_request(url: str, payloads: list, data: dict, login_dvwa: bool = False):
    if (login_dvwa):
        session = createSessionBwapp(URL)
    else:
        session = requests
    current_data = data.copy()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    for key, value in data.items():
        if (re.search("\$(.*?)\$", value) != None):
            v = postParser(value, payloads)
            current_data[key] = v
    
    processed_data = []
    for key, value in current_data.items():
        if (len(value) > 1 and isinstance(value, list)):
            for item in value:
                initial_data = data.copy()
                initial_data[key] = item
                processed_data.append(initial_data) # not a copy?
    
    result = []
    for index, value_dict in enumerate(processed_data):
        response = session.post(url, data = value_dict, headers=headers)
        status_code = response.status_code
        try:
            content_length = response.headers["Content-Length"]
        except:
            content_length = len(response.text)
        
        result.append([payloads[index], status_code, content_length]) 
        content_length = "0"
        status_code = 0
    return result


# if __name__ == "__main__":
    # payload 
    # post_request("https://bwapp.hakhub.net/sqli_6.php", payload, {"title": "$$", "action": "search"}, login_dvwa=True)