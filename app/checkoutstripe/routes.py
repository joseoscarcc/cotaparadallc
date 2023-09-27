from flask import render_template, jsonify,request, redirect
from app.checkoutstripe import bp
from app.extensions import db
from app.models.cpschema import Customer, Preorder, Order, OrderItem, Book
from datetime import datetime
import stripe
import os

STRIPE_TOKEN = os.environ.get('STRIPE_TOKEN')
ENDPOINT_SECRET = os.environ.get('ENDPOINT_SECRET')
STRIPE_PRICE_ID = os.environ.get('STRIPE_PRICE_ID')

@bp.route('/', methods=['GET', 'POST'])
def index():
    title="Checkout"
        
    return render_template('checkoutstripe/index.html',title=title)

@bp.route('/cart', methods=['GET', 'POST'])
def cart():

    stripe.api_key = STRIPE_TOKEN

    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']

    new_customer = Customer(first_name=nombre, last_name=apellido, email=correo, phone=telefono)
    # Add the new user to the database
    db.session.add(new_customer)
    db.session.flush()  # Flush to get the customer_id
    customer_id = new_customer.customer_id  # Get the auto-generated customer ID
    new_preorder = Preorder(customer_id = customer_id, book_id=1,payment_method_id=2,quantity=1,timestamp=datetime.utcnow(),status_id=4)
    db.session.add(new_preorder)
    db.session.flush()  # Flush to get the customer_id
    preorder_id = new_preorder.preorder_id  # Get the auto-generated customer ID
    db.session.commit()

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': STRIPE_PRICE_ID,
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_email = correo,
            client_reference_id=preorder_id,
            invoice_creation={'enabled':True},
            success_url='http://www.cotaparada.com/checkoutstripe/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://www.cotaparada.com/checkoutstripe/cancel',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
            return str(e)

    return redirect(checkout_session.url, code=303)

@bp.route('/success/', methods=['GET'])
def success():

    return render_template('checkoutstripe/success.html')

@bp.route('/cancel/', methods=['GET'])
def cancel():

    return render_template('checkoutstripe/cancel.html')

@bp.route('/webhook', methods=['POST'])
def webhook():

    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = ENDPOINT_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print("Invalid payload")
        return jsonify({'error': str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature")
        return jsonify({'error': str(e)}), 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session_id = event['data']['object']['id']
        session = stripe.checkout.Session.retrieve(session_id, expand=['line_items'])
        line_items = session['line_items']['data']
        session_01 = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(line_items, session_01)

    return jsonify({'message': 'Webhook received'}), 200

def fulfill_order(line_items, session_01):
    # Implement your order fulfillment logic here
    print(line_items)
    transfer_id = session_01.get("id")
    client_reference_id = session_01.get("client_reference_id")
    preorder = Preorder.query.filter_by(preorder_id=client_reference_id).first()
    book = Book.query.filter_by(book_id=preorder.book_id).first()
    precio_book_01 = book.price
    precio_book_02 = session_01.get("amount_total")/100
    if preorder:
         # Update the status to 1
        preorder.status_id = 1
        db.session.commit()
    
    # Create an Order instance
    order = Order(
        customer_id=preorder.customer_id,
        order_date=datetime.utcnow(),  # You may need to import datetime
        payment_method_id=preorder.payment_method_id,
        status_id=1,  # Status set to 1 as you mentioned
        transfer_id=transfer_id
    )

    # # Add these instances to the session and commit the changes
    db.session.add(order)
    db.session.flush()  # Flush to get the customer_id
    order_id = order.order_id 
    db.session.commit()

      # # Create an OrderItem instance
    order_item = OrderItem(
        order_id=order_id,
        book_id=preorder.book_id,
        quantity=preorder.quantity,
        discount=precio_book_02/precio_book_01,  # You may need to calculate the discount
        subtotal=precio_book_02*preorder.quantity  # Assuming this is the total amount from your JSON
    )

    db.session.add(order_item)
    db.session.commit()
