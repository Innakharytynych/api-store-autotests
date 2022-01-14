from pprint import pprint
import requests
from templates.req import transfer_template_func
from params import url_transfer, auth_key2
import pytest


'''позитивные тесты amount'''
@pytest.mark.parametrize('data_input', [
    transfer_template_func(amount='1.50000'),
    transfer_template_func(amount='0.00002'),
    transfer_template_func(amount='2.00000')
],
    ids=[
    'with dot',
    'min',
    'integer'
    ])
def test_transfer_correct_amount(data_input):
    r = requests.post(url=url_transfer, auth=auth_key2, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['transfer']['amount']['full_amount'] == data_input['amount']
    assert data['payload']['transfer']['currency']['name'] == transfer_template_func()['currency_name']
    assert data['payload']['transfer']['currency']['smart_contract'] == transfer_template_func()['currency_smart_contract']
    assert data['payload']['transfer']['receiver'] == transfer_template_func()['eos_account']
    assert data['payload']['transfer']['status'] == 'SENDED'
    assert data['status'] == 'OK'


'''позитивные тесты currency name'''
@pytest.mark.parametrize('data_input', [
    transfer_template_func(currency_name='USDCASH'),
    transfer_template_func(currency_name='RUBCASH'),
    transfer_template_func(currency_name='UAHCASH')
], ids=[
    'USDCASH token',
    'RUBCASH token',
    'UAHCASH token'
])
def test_transfer_correct_currency(data_input):
    r = requests.post(url=url_transfer, auth=auth_key2, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['transfer']['amount']['full_amount'] == transfer_template_func()['amount']
    assert data['payload']['transfer']['currency']['name'] == data_input['currency_name']
    assert data['payload']['transfer']['currency']['smart_contract'] == transfer_template_func()['currency_smart_contract']
    assert data['payload']['transfer']['id'] is not None
    assert data['payload']['transfer']['status'] == 'SENDED'
    assert data['status'] == 'OK'


'''трансфер для оплаты на смарт препрод'''
@pytest.mark.parametrize('data_input', [
    transfer_template_func(currency_smart_contract='kmp3wkgqfyqx')
], ids=[
    'preprod smart'
])
def test_transfer_currency_smart_contract(data_input):
    r = requests.post(url=url_transfer, auth=auth_key2, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['transfer']['amount']['full_amount'] == transfer_template_func()['amount']
    assert data['payload']['transfer']['currency']['name'] == transfer_template_func()['currency_name']
    assert data['payload']['transfer']['currency']['smart_contract'] == data_input['currency_smart_contract']
    assert data['payload']['transfer']['id'] is not None
    assert data['payload']['transfer']['status'] == 'SENDED'
    assert data['status'] == 'OK'

    '''позитивные тесты currency name'''


@pytest.mark.parametrize('data_input', [
    transfer_template_func(eos_account='testov.pcash'),
    transfer_template_func(eos_account='515253545553'),
    transfer_template_func(eos_account='fletchercat1')
], ids=[
    'with .pcash',
    'only number',
    'letters + numbers '
])
def test_transfer_correct_currency(data_input):
    r = requests.post(url=url_transfer, auth=auth_key2, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['payload']['transfer']['receiver'] == data_input['eos_account']
    assert data['payload']['transfer']['sender'] == '141111.pcash'
    assert data['payload']['transfer']['id'] is not None
    assert data['payload']['transfer']['status'] == 'SENDED'
    assert data['payload']['transfer']['txn_type'] == 'WITHDRAW'
    assert data['status'] == 'OK'


'''негативные тесты amount'''
@pytest.mark.parametrize('data_input', [
    transfer_template_func(''),
    transfer_template_func('0.0000001'),
    transfer_template_func('ghjghjh'),
    transfer_template_func('££"$%%^^$%'),
    transfer_template_func('0.00000'),
    transfer_template_func('999999'),
    transfer_template_func('10,30000'),
    transfer_template_func('0.00001'),
    transfer_template_func('-1')
],
    ids=[
    'none',
    'min-min',
    'letter',
    'symbol',
    'zero',
    'max-max',
    'with coma',
    'min',
    'negative amount'
    ])
def test_transfer_incorrect_amount(data_input):
    r = requests.post(url=url_transfer, auth=auth_key2, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['status'] == 'ERROR'
    if data['error'] == 'Params is empty or have invalid format':
        assert True
    elif data['error'] == 'Min available amount is 0.00002':
        assert True
    else:
        assert data['error'] == 'The amount on your account is not enough to complete the transaction'


'''негативные тесты currency name'''
@pytest.mark.parametrize('data_input', [
    transfer_template_func(currency_name=''),
    transfer_template_func(currency_name='RMBCASH'),
    transfer_template_func(currency_name='EURCASH'),
    transfer_template_func(currency_name='text'),
    transfer_template_func(currency_name='345667'),
    transfer_template_func(currency_name='RUB')

], ids=[
    'None',
    'RMBCASH token',
    'EURCASH token',
    'text',
    '4556545',
    'RUB'

])
def test_transfer_incorrect_currency(data_input):
    r = requests.post(url=url_transfer, auth=auth_key2, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['error'] == 'Currency not found'
    assert data['status'] == 'ERROR'


'''негативные тесты смарт-контракт'''
@pytest.mark.parametrize('data_input', [
    transfer_template_func(currency_smart_contract=''),
    transfer_template_func(currency_smart_contract='gjghjhjhj'),
    transfer_template_func(currency_smart_contract='23233243345'),
    transfer_template_func(currency_smart_contract='token.pcash'),
    transfer_template_func(currency_smart_contract='££"$%%^^$%'),
    transfer_template_func(currency_smart_contract='mechatmechat'),
    transfer_template_func(currency_name='jqpua4jqkqwz')

], ids=[
    'None',
    'text',
    '23233243345',
    'prod smart p2p',
    'symbol',
    'prod smart another',
    'preprod smart another'

])
def test_transfer_incorrect_currency_smart_contract(data_input):
    r = requests.post(url=url_transfer, auth=auth_key2, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['error'] == 'Currency not found'
    assert data['status'] == 'ERROR'


'''негативные тесты получатель'''
@pytest.mark.parametrize('data_input', [
    transfer_template_func(eos_account=''),
    transfer_template_func(eos_account='333333333'),
    transfer_template_func(eos_account='££"$%%^^$%')

], ids=[
    'None',
    'not exist',
    'symbol'
])
def test_transfer_incorrect_currency_eos_account(data_input):
    r = requests.post(url=url_transfer, auth=auth_key2, json=data_input)
    data = r.json()

    assert r.status_code == 200
    assert data['error'] == 'Eos account does not exists in blockchain'
    assert data['status'] == 'ERROR'