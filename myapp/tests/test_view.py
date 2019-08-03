# -*- coding: utf-8 -*-


# open page
# check fields: summ, currency(EUR, RUB, USD), description
# check button
import re

from myapp.models import Transaction
from myapp.utils import generate_sign, check_data_valid


def test_view_GET(client):
    # open page
    body = client.get('/').data.decode('utf-8')

    # check fields: sum, currency, description
    for id in ['sum', 'currency', 'description']:
        assert re.search(r'<(input|select)[^>]+id="{}"'.format(id), body), "{} Not found".format(id)

    # check button
    assert '<input class="btn btn-success mt-3" value="Оплатить" type="submit"/>' in body, 'button not found'


def test_sign():
    transaction = Transaction(amount=10.0, currency=643, id=101)
    expected_result = '15c02fb3f107c59c151cd1dc6f920bf7c35c3e8a2ffe90e18e2a8a8dd4b2ac16'

    actual_result = generate_sign(transaction, payeer_rub=True)

    assert expected_result == actual_result


def test_data_valid():
    form_data_invalid = {'currency': '', 'amount': '46.50'}
    form_data_valid = {'currency': '643', 'amount': '46.50'}

    #actual_result1 = check_data_valid(form_data_invalid)

    assert check_data_valid(form_data_invalid) is False, 'invalid test is down'

    assert check_data_valid(form_data_valid) is True, 'valid test is down'



__author__ = 'manitou'
