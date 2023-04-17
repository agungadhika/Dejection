import requests
from .parse import parser
from requests.utils import requote_uri
from bs4 import BeautifulSoup as bs4

def findInput(url):
    # s = createSession(URL)
    # content = s.get(url).content
    content = requests.get(url).content
    soup = bs4(content, "html.parser")
    input_form = soup.find_all("input")
    return [i.get("name") for i in input_form if i.get("name") is not None]

context_data = {}
def post_validation(url: str, type_attack: str):
    global context_data
    input_id = findInput(url)
    context_data = {
        "url": url,
        "input_id": input_id,
        "type_attack": type_attack
    }
    return context_data

def post_request(url: str, payloads: list):
    pass