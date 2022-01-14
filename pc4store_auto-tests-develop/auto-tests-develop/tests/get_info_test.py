from pprint import pprint
import requests
from params import *
from templates.req import create_template_func


"""получить инфо по заказу"""
def test_get_info():
    r = requests.post(url=url_create, auth=auth_key, json=create_template_func())
    data = r.json()
    resp = requests.get(url=url_get_info(data['payload']['order']['id']), auth=auth_key)
    data2 = resp.json()
    pprint(data2)

#TODO: основа готова, написать тесты для состояний см. доку