from pprint import pprint
import pytest
import requests
import params
from datetime import datetime, timedelta
from params import url_create, auth_key
from templates.req import create_template, create_template_func


"""позитивные тесты amount to pay"""
@pytest.mark.parametrize('data_input', [
    create_template_func(amount_to_pay='0.00002'),
    create_template_func(amount_to_pay='11.70000'),
    create_template_func(amount_to_pay='15.00000'),
    create_template_func(amount_to_pay='1000000000.00000'),
    create_template_func(amount_to_pay='1000000001.00000')
], ids=[
    'minimum amount to pay',
    'amount with dot',
    'integer amount',
    'front max amount',
    'more than front max'
])
def test_create_order_field_amount_to_pay(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == data_input['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == create_template_func()["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""позитивные тесты max fee"""
@pytest.mark.parametrize('data_input', [
    create_template_func(amount_to_pay='99999.00000'),
    create_template_func(amount_to_pay='100000.00000'),
    create_template_func(amount_to_pay='110000.00000')
], ids=[
    'fee = 249.99750',
    'fee = 250.00000',
    'max fee = 250.00000'
])
def test_create_order_check_fee(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == data_input['amount_to_pay']
    if data_input['amount_to_pay'] == '99999.00000':
        assert data['payload']['order']['amount']['fee'] == '249.99750'
    elif data_input['amount_to_pay'] == '100000.00000':
        assert data['payload']['order']['amount']['fee'] == '250.00000'
    else:
        assert data['payload']['order']['amount']['fee'] == '250.00000'
    assert data['payload']['order']['currency']['name'] == create_template_func()["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""позитивные тесты currency name"""
@pytest.mark.parametrize('data_input', [
    create_template_func(currency_name='USDCASH'),
    create_template_func(currency_name='RUBCASH'),
    create_template_func(currency_name='UAHCASH')
], ids=[
    'USDCASH token',
    'RUBCASH token',
    'UAHCASH token',
])
def test_create_order_field_currency_name(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == create_template_func()['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == data_input["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""тест создания заказа для оплаты на смарт препрод"""
def test_create_order_currency_smart_contract(create_template):
    create_template["currency_smart_contract"] = 'kmp3wkgqfyqx'
    r = requests.post(url=url_create, auth=auth_key, json=create_template)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == create_template_func()['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == create_template_func()['currency_name']
    assert data['payload']['order']['currency']['smart_contract'] == create_template["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""позитивные тесты response url"""
@pytest.mark.parametrize('data_input', [
    create_template_func(response_url='https://www.aruma.com.au/wp-content/uploads/2016/04/question-unsplash.jpg.webp'),
    create_template_func(response_url=''),
    create_template_func(response_url='text without URL'),
    create_template_func(response_url='!@#$%^& *(),. symbols'),
    create_template_func(response_url='1234 integer'),

], ids=[
    'url',
    'empty field',
    'text without URL',
    'special in text',
    'number in text'
])
def test_create_order_field_response_url(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == create_template_func()['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == create_template_func()["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == data_input['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""позитивные тесты merchant order id"""
@pytest.mark.parametrize('data_input', [
    create_template_func(merchant_order_id='just text'),
    create_template_func(merchant_order_id=''),
    create_template_func(merchant_order_id='text with 12345678'),
    create_template_func(merchant_order_id='!@#$%^& *(),. symbols')
], ids=[
    'text',
    'empty field',
    'numbers in text',
    'special in text'
])
def test_create_order_field_merchant_order_id(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == create_template_func()['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == create_template_func()["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == data_input['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""позитивные тесты description"""
@pytest.mark.parametrize('data_input', [
    create_template_func(description='just text'),
    create_template_func(description=''),
    create_template_func(description='text with 12345678'),
    create_template_func(description='!@#$%^& *(),. symbols')
], ids=[
    'text',
    'empty field',
    'numbers in text',
    'special in text'
])
def test_create_order_field_description(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == create_template_func()['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == create_template_func()["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == data_input['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""позитивные тесты expiration time"""
@pytest.mark.parametrize('data_input', [
    create_template_func(expiration_time=1),
    create_template_func(expiration_time=2),
    create_template_func(expiration_time=99999998),
    create_template_func(expiration_time=99999999)
], ids=[
    'minimum time',
    'time',
    'less than max time',
    'max time'
])
def test_create_order_field_expiration_time(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    my_calc_expiration_time = (datetime.utcnow() + timedelta(minutes=data_input['expiration_time'])). \
        strftime('%Y, %m, %d, %H, %M')
    answer_expiration_time = datetime.fromisoformat(data['payload']['order']['expiration_date']). \
        strftime('%Y, %m, %d, %H, %M')

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == create_template_func()['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == create_template_func()["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert my_calc_expiration_time == answer_expiration_time
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""позитивные тесты success payment redirect url"""
@pytest.mark.parametrize('data_input', [
    create_template_func(success_payment_redirect_url=
                         'https://cdn.icon-icons.com/icons2/10/PNG/256/check_ok_accept_apply_1582.png'),
    create_template_func(success_payment_redirect_url='just text'),
    create_template_func(success_payment_redirect_url=''),
    create_template_func(success_payment_redirect_url='text with 12345678'),
    create_template_func(success_payment_redirect_url='!@#$%^& *(),. symbols')
], ids=[
    'URL',
    'text',
    'empty field',
    'numbers in text',
    'special in text'
])
def test_create_order_field_success_payment_redirect_url(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == create_template_func()['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == create_template_func()["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           create_template_func()["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           data_input['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""позитивные тесты failed payment redirect url"""
@pytest.mark.parametrize('data_input', [
    create_template_func(failed_payment_redirect_url=
                         'https://upload.wikimedia.org/wikipedia/commons/4/4e/Fail_stamp.jpg'),
    create_template_func(failed_payment_redirect_url='just text'),
    create_template_func(failed_payment_redirect_url=''),
    create_template_func(failed_payment_redirect_url='text with 12345678'),
    create_template_func(failed_payment_redirect_url='!@#$%^& *(),. symbols')
], ids=[
    'URL',
    'text',
    'empty field',
    'numbers in text',
    'special in text'
])
def test_create_order_field_failed_payment_redirect_url(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['order']['amount']['full_amount'] == create_template_func()['amount_to_pay']
    assert data['payload']['order']['currency']['name'] == create_template_func()["currency_name"]
    assert data['payload']['order']['currency']['smart_contract'] == create_template_func()["currency_smart_contract"]
    assert data['payload']['order']['expiration_date'] is not None
    assert data['payload']['order']['details']['merchant_order_id'] == create_template_func()['merchant_order_id']
    assert data['payload']['order']['details']['description'] == create_template_func()['description']
    assert data['payload']['order']['failed_payment_redirect_url'] == \
           data_input["failed_payment_redirect_url"]
    assert data['payload']['order']['id'] is not None
    assert data['payload']['order']['is_test'] is False
    assert data['payload']['order']['payment_url'] == params.payment_url + data['payload']['order']['id']
    assert data['payload']['order']['response_url'] == create_template_func()['response_url']
    assert data['payload']['order']['sequent_number'] is not None
    assert data['payload']['order']['status'] == 'CREATED'
    assert data['payload']['order']['success_payment_redirect_url'] == \
           create_template_func()['success_payment_redirect_url']
    assert data['status'] == 'OK'


"""негативные тесты amount to pay"""
@pytest.mark.parametrize('data_input', [
    create_template_func(amount_to_pay=''),
    create_template_func(amount_to_pay='0.00000'),
    create_template_func(amount_to_pay='0.00001'),
    create_template_func(amount_to_pay='0.0000002'),
    create_template_func(amount_to_pay='text'),
    create_template_func(amount_to_pay='!@#$%^& *(),.'),
    create_template_func(amount_to_pay='10,3'),
    create_template_func(amount_to_pay='-1')
], ids=[
    'empty amount',
    'null amount',
    'amount < minimum',
    'precision > 5',
    'string',
    'special symbols',
    'amount with comma',
    'negative number'

])
def test_neg_create_order_field_amount_to_pay(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    try:
        assert data['error'] == 'Params is empty or have invalid format'
    except:
        assert data['error'] == 'Min available amount is 0.00002'
    assert data['status'] == 'ERROR'


"""негативные тесты currency name"""
@pytest.mark.parametrize('data_input', [
    create_template_func(currency_name=''),
    create_template_func(currency_name='EURCASH'),
    create_template_func(currency_name='text'),
    create_template_func(currency_name='!@#$%^& *(),.'),
    create_template_func(currency_name=1234)
], ids=[
    'empty name',
    'EURO token',
    'string',
    'special',
    'integer'
])
def test_neg_create_order_field_currency_name(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    try:
        assert data['error'] == 'Currency not found'
    except:
        assert data['error'] == 'Opps, Something wrong...'

    assert data['status'] == 'ERROR'


"""негативные тесты currency smart contract"""
@pytest.mark.parametrize('data_input', [
    create_template_func(currency_smart_contract=''),
    create_template_func(currency_smart_contract='token.pcash'),
    create_template_func(currency_smart_contract='text'),
    create_template_func(currency_smart_contract='!@#$%^& *(),.'),
    create_template_func(currency_smart_contract=1234)
], ids=[
    'empty name',
    'prod smart contract',
    'string',
    'special',
    'integer'
])
def test_neg_create_order_field_currency_smart_contract(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    try:
        assert data['error'] == 'Currency not found'
    except:
        assert data['error'] == 'Opps, Something wrong...'
    assert data['status'] == 'ERROR'


"""негативные тесты currency response url"""
@pytest.mark.parametrize('data_input', [
    create_template_func(response_url=1234)
], ids=[
    'integer'
])
def test_neg_create_order_field_response_url(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['error'] == 'Opps, Something wrong...'
    assert data['status'] == 'ERROR'


"""негативные тесты merchant order id"""
@pytest.mark.parametrize('data_input', [
    create_template_func(merchant_order_id=1234)
], ids=[
    'integer'
])
def test_neg_create_order_field_merchant_order_id(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['error'] == 'Opps, Something wrong...'
    assert data['status'] == 'ERROR'


"""негативные тесты description"""
@pytest.mark.parametrize('data_input', [
    create_template_func(description=1234)
], ids=[
    'integer'
])
def test_neg_create_order_field_description(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['error'] == 'Opps, Something wrong...'
    assert data['status'] == 'ERROR'


"""позитивные тесты expiration time"""
@pytest.mark.parametrize('data_input', [
    create_template_func(expiration_time=None),
    create_template_func(expiration_time=0),
    create_template_func(expiration_time=100000000),
    create_template_func(expiration_time=-10)
], ids=[
    'none',
    'zero +15',
    'more than max time +99999999',
    'negative time'
])
def test_create_order_field_expiration_time(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()
    "не забыть убрать строку после написания assert"
    pprint(data)

    my_calc_expiration_time = (datetime.utcnow() + timedelta(minutes=data_input['expiration_time'])). \
        strftime('%Y, %m, %d, %H, %M')
    answer_expiration_time = datetime.fromisoformat(data['payload']['order']['expiration_date']). \
        strftime('%Y, %m, %d, %H, %M')

# TODO: дописать assert когда Саша исправит отрицательное время


"""негативные тесты success payment redirect url"""
@pytest.mark.parametrize('data_input', [
    create_template_func(success_payment_redirect_url=1234)
], ids=[
    'integer'
])
def test_neg_create_order_field_success_payment_redirect_url(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['error'] == 'Opps, Something wrong...'
    assert data['status'] == 'ERROR'


"""негативные тесты failed payment redirect url"""
@pytest.mark.parametrize('data_input', [
    create_template_func(failed_payment_redirect_url=1234)
], ids=[
    'integer'
])
def test_neg_create_order_field_failed_payment_redirect_url(data_input):
    r = requests.post(url=url_create, auth=auth_key, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['error'] == 'Opps, Something wrong...'
    assert data['status'] == 'ERROR'
