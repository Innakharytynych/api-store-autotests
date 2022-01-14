"""URLS"""
url_base = 'https://api.test.pc4.store/'
url_create = 'https://api.test.pc4.store/v1/create'
url_transfer = 'https://api.test.pc4.store/v1/transfer'
payment_url = 'https://test.pc4.store/payment/'

def url_get_info(order_id):
    url_get_info_link = f'https://api.test.pc4.store/v1/order_info/{order_id}'
    return url_get_info_link


"""BasicAuth"""
auth_key = (
    'e064c7f5-2bf0-40f8-98f0-eb60ea32ae68',
    'f80aa7c8-23a2-456e-a200-50c8540b6048'
)

auth_key2 = (
    '8a064f58-a22a-48ea-b380-37b6556e083d',
    'bb0425ce-02a6-44c4-993e-10b8433c5b4d')
