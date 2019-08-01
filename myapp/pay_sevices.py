import json
import requests
from myapp import db
from myapp.utils import generate_sign
from .models import Transaction


class PayService:
    tr = None
    html_file = 'pay.html'

    def __init__(self, post_data):
        self.post_data = post_data

    def start_transaction(self):
        self.post_data['amount'] = round(float(self.post_data['amount']), 2)
        self.tr = Transaction(**self.post_data)
        db.session.add(self.tr)
        db.session.flush()

    def send_request(self):
        pass

    def format_template_data(self):
        print(self.tr.amount, type(self.tr.amount))
        pass

    @property
    def success_request(self):
        self.tr.status = True
        db.session.commit()
        return True

    @property
    def sign(self):
        return generate_sign(self.tr)


class PiastrixService(PayService):
    request = None
    response_data = None
    request_data = None
    url = 'https://core.piastrix.com/bill/create'
    headers = {'Content-Type': 'application/json'}

    def set_request_data(self):
        data = {
            'payer_currency': int(self.tr.currency),
            'shop_amount': str(self.tr.amount),
            'shop_currency': int(self.tr.currency),
            'shop_id': '5',
            'shop_order_id': self.tr.id,
            'sign': self.sign,
        }
        if self.tr.description:
            data['description'] = self.tr.description
        print(data, type(data['shop_id']))
        self.request_data = json.dumps(data)

    def send_request(self):
        self.set_request_data()
        self.request = requests.post(self.url, headers=self.headers, data=self.request_data)
        self.response_data = json.loads(self.request.content)
        print(self.response_data)

    @property
    def success_request(self):
        if self.response_data['result']:
            self.tr.payment_id = self.response_data['data']['id']
            self.tr.status = True
            db.session.commit()
        return self.response_data['result']

    @property
    def redirect_url(self):
        return self.response_data['data']['url']

    @property
    def sign(self):
        return generate_sign(self.tr, usd=True)

class PayeerService(PiastrixService):
    tmp = {}
    html_file = 'invoice.html'
    url = 'https://core.piastrix.com/invoice/create'

    def set_request_data(self):
        data = {
            'shop_id': 5,
            'sign': self.sign,
            'payway': 'payeer_rub',
            'amount': self.tr.amount,
            'shop_order_id': self.tr.id,
            'currency': self.tr.currency,
        }
        if self.tr.description:
            data['description'] = self.tr.description
        self.request_data = json.dumps(data)

    def format_template_data(self):
        self.tmp['url'] = self.response_data['data']['url']
        self.tmp['method'] = self.response_data['data']['method']
        self.tmp['referer'] = self.response_data['data']['data']['referer']
        self.tmp['m_historyid'] = self.response_data['data']['data']['m_historyid']
        self.tmp['m_historytm'] = self.response_data['data']['data']['m_historytm']
        self.tmp['m_curorderid'] = self.response_data['data']['data']['m_curorderid']

    @property
    def sign(self):
        return generate_sign(self.tr, payeer_rub=True)
