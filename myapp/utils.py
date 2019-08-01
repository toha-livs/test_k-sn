import hashlib


def check_data_valid(request_data):
    valid_key = ['currency', 'amount']
    for key in valid_key:
        if not request_data.get(key):
            return False
    return True


def generate_sign(transaction, amount, rub=False):
    payeer_rub = ('', 'payeer_rub:')[rub]
    line = '{}:{}:{}5:{}SecretKey01'.format(amount, transaction.currency, payeer_rub, transaction.id)
    return hashlib.sha256(line.encode('utf-8')).hexdigest()
