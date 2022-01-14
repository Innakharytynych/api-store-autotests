import pytest


@pytest.fixture()
def create_template():
    return create_template_func()


def create_template_func(amount_to_pay='100.50000',
                         currency_name='USDCASH',
                         currency_smart_contract='kmp3wkgqfyqx',
                         response_url='',
                         merchant_order_id='',
                         description='',
                         expiration_time=20,
                         success_payment_redirect_url='',
                         failed_payment_redirect_url=''):

    return {"amount_to_pay": amount_to_pay,
            "currency_name": currency_name,
            "currency_smart_contract": currency_smart_contract,
            "response_url": response_url,
            "merchant_order_id": merchant_order_id,
            "description": description,
            "expiration_time": expiration_time,
            "success_payment_redirect_url": success_payment_redirect_url,
            "failed_payment_redirect_url": failed_payment_redirect_url
            }


@pytest.fixture()
def transfer_template():
    return transfer_template_func()


def transfer_template_func(amount='0.05000',
                           currency_name='USDCASH',
                           currency_smart_contract='kmp3wkgqfyqx',
                           eos_account='333334.pcash'):
    return {
        'amount': amount,
        'currency_name': currency_name,
        'currency_smart_contract': currency_smart_contract,
        'eos_account': eos_account}