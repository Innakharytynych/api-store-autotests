from pprint import pprint
import requests
from params import *
from templates.mutations import *
from templates.req import create_template_func


"""Нажатие кнопки Успешная оплата (MONEY_RECEIVED, транзакция reversible)"""
def test_btn_successful_payment_mr():
    r = requests.post(url=url_create, auth=auth_key, json=create_template_func())
    data = r.json()

    r = requests.post(url=url_base, json=mutation_successful_payment(data['payload']['order']['id']))
    data2 = r.json()

    assert data2['data']['testPayment']['__typename'] == 'TestPaymentSuccess'
    assert data2['data']['testPayment']['order']['__typename'] == 'OrderNode'
    assert data2['data']['testPayment']['order']['id'] == data['payload']['order']['id']
    assert data2['data']['testPayment']['order']['status'] == 'MONEY_RECEIVED'


"""Нажатие кнопки Отмена"""
def test_btn_cancel():
    r = requests.post(url=url_create, auth=auth_key, json=create_template_func())
    data = r.json()

    r = requests.post(url=url_base, json=mutation_cancel(data['payload']['order']['id']))
    data2 = r.json()

    assert data2['data']['testCancelOrder']['__typename'] == 'CancelOrderSuccess'
    assert data2['data']['testCancelOrder']['order']['__typename'] == 'OrderNode'
    assert data2['data']['testCancelOrder']['order']['id'] == data['payload']['order']['id']
    assert data2['data']['testCancelOrder']['order']['status'] == 'CANCELLED'


"""Нажатие кнопки Время истекло"""
def test_btn_expired():
    r = requests.post(url=url_create, auth=auth_key, json=create_template_func())
    data = r.json()

    r = requests.post(url=url_base, json=mutation_expired(data['payload']['order']['id']))
    data2 = r.json()

    pprint(data2)

    assert data2['data']['testExpire']['__typename'] == 'TestExpireSuccess'
    assert data2['data']['testExpire']['order']['__typename'] == 'OrderNode'
    assert data2['data']['testExpire']['order']['id'] == data['payload']['order']['id']
    assert data2['data']['testExpire']['order']['status'] == 'EXPIRED'