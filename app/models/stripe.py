import stripe
from flask import url_for

stripe_public_key = 'pk_test_51NFkrvDKwG3GlPeGzqOoOUO1mHUsrDqp2cXHPzhdhFQRxgmulbvd5ph0oJ1nBEN37tjcmxmEjkFkJWaWqTM3sIFe00agLmBaHv'
stripe_secret_key = 'sk_test_51NFkrvDKwG3GlPeGfQKnC7sb9efwZ4A3VHlDEvVgQvvufxbbELNJzE9WCvng9zIsg0cEgOq96cEYnnp76tjiULPe00RyJbh9P2'

YOUR_DOMAIN = 'http://www.cotaparda.com'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1Nv7lpDKwG3GlPeGHKl7IlZt',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('thanks', _external=True),
            cancel_url=url_for('index', _external=True),
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
