import datetime

from . import db


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float(2))
    currency = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    description = db.Column(db.String(32))
    payment_id = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Transaction: id={}, amount={}, date={}, currency={}, description={}, payment_id={}, status={}'.format(
                                                                                                        self.id,
                                                                                                        self.amount,
                                                                                                        self.date,
                                                                                                        self.currency,
                                                                                                        self.description,
                                                                                                        self.payment_id,
                                                                                                        self.status)
