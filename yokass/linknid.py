from yookassa.configuration import Configuration
from yookassa.payment import Payment
import uuid

Configuration.account_id = ''
Configuration.secret_key = ''

def create(amount, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
    "amount": {
        "value": amount,
        "currency": "RUB"
    },
    'payment_method_data':{
        'type': 'bank_card'
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://t.me/d2stylish_bot"
    },
    "capture": True,
    "description": "Тест",
    "metadata": {
      'chat_id': chat_id
    },
}, id_key)
    
    return payment.confirmation.confirmation_url, payment.id

def check(payment_id):
    payment = Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return payment.metadata
    else:
        return False
