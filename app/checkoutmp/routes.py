from flask import render_template, jsonify,request, current_app
from app.checkoutmp import bp
from app.extensions import db
from app.models.cpschema import Customer, Preorder, Order, OrderItem, Book
from datetime import datetime
import mercadopago
import os

MP_TOKEN = os.environ.get('MP_TOKEN')
MP_TOKEN_DEV = os.environ.get('MP_TOKEN_DEV')

sdk = mercadopago.SDK(MP_TOKEN)

@bp.route('/', methods=['GET', 'POST'])
def index():
    title="Checkout"
        
    return render_template('checkoutmp/index.html',title=title)

@bp.route('/carrito', methods=['GET', 'POST'])
def carrito():

    nombre = request.form['nombre']
    apellido = request.form['apellido']
    telefono = request.form['telefono']
    correo = request.form['correo']

    new_customer = Customer(first_name=nombre, last_name=apellido, email=correo, phone=telefono)
    # Add the new user to the database
    db.session.add(new_customer)
    db.session.flush()  # Flush to get the customer_id
    customer_id = new_customer.customer_id  # Get the auto-generated customer ID
    new_preorder = Preorder(customer_id = customer_id, book_id=1,payment_method_id=1,quantity=1,timestamp=datetime.utcnow(),status_id=4)
    db.session.add(new_preorder)
    db.session.flush()  # Flush to get the customer_id
    preorder_id = new_preorder.preorder_id  # Get the auto-generated customer ID
    db.session.commit()
    # Crea un ítem en la preferencia
    preference_data = {
        "items": [
        {
            "id": "item-ID-0004",
            "title": "Quiero Viajar Más",
            "currency_id": "MXN",
            "description": "Libro sobre los viajes de JOE",
            "category_id": "libros",
            "quantity": 1,
            "unit_price": 215.00
        }
    ],
    "payer": {
        "name": nombre,
        "surname": apellido,
        "email": correo,
        "phone": {
            "number": telefono
        },
    },
    "back_urls": {
        "success": "http://127.0.0.1:5000/checkoutmp/success",
        "failure": "http://127.0.0.1:5000/checkoutmp/failure",
        "pending": "http://127.0.0.1:5000/checkoutmp/pending"
    },
    "statement_descriptor": "CotaParadaLLC",
    "external_reference": preorder_id,
    "notification_url" : "http://requestbin.fullcontact.com/1ogudgk1",
}

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    preference_id = preference["id"]

    return render_template('checkoutmp/checkout.html',preference_id=preference_id,email=correo, MP_TOKEN_DEV=MP_TOKEN_DEV)

@bp.route('/success/', methods=['GET'])
def success():
    # Get the values of the query parameters from the URL
    collection_id = request.args.get('collection_id')
    collection_status = request.args.get('collection_status')
    payment_id = request.args.get('payment_id')
    status = request.args.get('status')

    # Now you can use these variables in your code as needed
    # For example, you can print them to see the values
    print(f"Collection ID: {collection_id}")
    print(f"Collection Status: {collection_status}")
    print(f"Payment ID: {payment_id}")
    print(f"Status: {status}")

    return render_template('checkoutmp/success.html',collection_id=collection_id,
                           collection_status=collection_status,
                           payment_id=payment_id,
                           status=status)
@bp.route('/webhook/', methods=['GET'])
def webhook():
    # Get the POST data
    data = request.json

    # Check the notification type
    notification_type = data.get('type')

    if notification_type == 'payment':
        payment_id = data['data']['id']
        preorder_id = data['data']['external_reference']
        payment_info = sdk.get_payment(payment_id)
        payment_amount = data['data']['payments']['total_paid_amount']

        print(payment_id)
        print(payment_info)
        # Fulfill the purchase...
        fulfill_order(payment_id, preorder_id, payment_amount)
        return jsonify({'message': 'Webhook received'}), 200

def fulfill_order(payment_id, preorder_id, payment_amount):
    # Implement your order fulfillment logic here
    print(payment_id)
    transfer_id = payment_id
    client_reference_id = preorder_id
    preorder = Preorder.query.filter_by(preorder_id=client_reference_id).first()
    book = Book.query.filter_by(book_id=preorder.book_id).first()
    precio_book_01 = book.price
    precio_book_02 = payment_amount
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

    print("Fulfilling order")