import hashlib


def check_data_valid(request_data):
    valid_key = ['currency', 'amount']
    for key in valid_key:
        if not request_data.get(key):
            return False
    return True


def generate_sign(transaction, **kwargs):
    usd = ('', '{}:'.format(transaction.currency))[bool(kwargs.get('usd'))]
    payeer_rub = ('', 'payeer_rub:')[bool(kwargs.get('payeer_rub'))]
    line = '{}{}:{}:{}5:{}SecretKey01'.format(usd, transaction.amount, transaction.currency, payeer_rub, transaction.id)
    print(line)
    return hashlib.sha256(line.encode('utf-8')).hexdigest()
