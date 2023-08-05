import urllib
from bs4 import BeautifulSoup

def convert_list_to_string(input_list: list, separator=",") -> str:
    """
    Converts a list to a string with a separator
    """
    return separator.join(input_list)


def convert_list_to_dict(input_list: list, key: str = "id") -> dict:
    """
    Converts a list to a dictionary.
    Arguments:
        :param input_list(list): The list to be converted
        :param key(str): The key of each item in list to be promoted
    """
    return {item[key]: item for item in input_list}

def convert_ids(ids) -> str:
    if type(ids) == str:
        return ids
    elif type(ids) == list:
        return ",".join(ids)
    elif ids == None:
        return ""

def convert_parameters(parameters) -> str:
    if parameters == None or type(parameters) != dict:
        return ""
    else:
        return f"?{urllib.parse.urlencode(parameters)}" if parameters != None else ""

def get_custom_field(response: dict, customfieldId: str) -> str:
    customField = [d["value"] for d in response["customFields"] if d["id"] == customfieldId]
    if len(customField) > 0:
        return customField[0]
    else:
        return None

def clean_html(tags, html):
    soup = BeautifulSoup(html,'html.parser')
    for ch in soup.find_all():
        if ch.name not in tags:
            ch.unwrap()
    return soup