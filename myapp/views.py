from flask import render_template, request, redirect

from myapp.utils import check_data_valid
from . import app
from .pay_sevices import PayeerService, PiastrixService, PayService

payment_service = {
    '978': PayService,
    '840': PiastrixService,
    '643': PayeerService
}


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        if check_data_valid(request.form):
            payment = payment_service[request.form['currency']](request.form.to_dict())
            payment.start_transaction()
            payment.send_request()
            if payment.success_request:
                if request.form['currency'] == '840':
                    return redirect(payment.redirect_url)
                else:
                    payment.format_template_data()
                    return render_template(payment.html_file, transaction=payment)
        return 'bad request', 400
    else:
        return render_template('root.html')
