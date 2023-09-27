from flask import render_template, jsonify, request
from app.checkoutmp import bp
from app.extensions import db
from app.models.cpschema import Customer, Preorder, Order, OrderItem, Book
from datetime import datetime
import mercadopago
import requests
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
        "success": "http://www.cotaparada.com/checkoutmp/success",
        "failure": "http://www.cotaparada.com/checkoutmp/failure",
        "pending": "http://www.cotaparada.com/checkoutmp/pending"
    },
    "statement_descriptor": "CotaParadaLLC",
    "external_reference": preorder_id,
    "notification_url" : "http://www.cotaparada.com/checkoutmp/webhook",
}

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    preference_id = preference["id"]

    return render_template('checkoutmp/checkout.html',preference_id=preference_id,email=correo, MP_TOKEN_DEV=MP_TOKEN_DEV)

@bp.route('/success/', methods=['GET', 'POST'])
def success():
    # Get the values of the query parameters from the URL
    collection_id = request.args.get('collection_id')
    collection_status = request.args.get('collection_status')
    payment_id = request.args.get('payment_id')
    status = request.args.get('status')
    external_reference = request.args.get('external_reference')
    if status == 'approved':
        fulfill_order(payment_id, external_reference)
        return render_template('checkoutmp/success.html',collection_id=collection_id,
                           collection_status=collection_status,
                           payment_id=payment_id,
                           status=status)
    else:
        return render_template('checkoutmp/failed.html')

@bp.route('/webhook', methods=['POST'])
def webhook():

    # Get the POST data as JSON
    data = requests.json
    print(data)
    # Check the notification type
    notification_type = data.get('type')
    print(notification_type)
    external_reference = data.get("external_reference")
    print(external_reference)
    try:
        if notification_type == 'payment':
            payment = sdk.Payment.find_by_id(data['data']['id'])
            print(f"a traves del webhook {payment}")


        elif notification_type == 'plan':
            plan = sdk.Plan.find_by_id(data['data']['id'])
        elif notification_type == 'subscription':
            subscription = sdk.Subscription.find_by_id(data['data']['id'])
        elif notification_type == 'invoice':
            invoice = sdk.Invoice.find_by_id(data['data']['id'])
        elif notification_type == 'point_integration_wh':
            # Handle point integration webhook data
            pass
        else:
            # Handle other notification types if needed
            pass

        return jsonify({'message': 'Webhook received'}), 200

    except mercadopago.exceptions.MPException as e:
        # Handle exceptions from Mercado Pago SDK
        return jsonify({'error': str(e)}), 500

def fulfill_order(payment, external_reference):
    # Define your MercadoPago API endpoint and access token
    print("enter fullfilment function")
    api_url = f'https://api.mercadopago.com/v1/payments/{payment}'  # Replace {id} with the actual payment ID
   
    # Set up the headers with the Authorization token
    headers = {
        'Authorization': f'Bearer {MP_TOKEN}'
    }

    # Make the GET request
    try:
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # You can access the response data as JSON
            payment_data = response.json()
            transfer_id = payment
            client_reference_id = external_reference
            total_paid_amount = payment_data['transaction_details']['total_paid_amount']
            external_reference = payment_data['external_reference']
            print(payment_data)
            print(client_reference_id)
            print(external_reference)
            print(total_paid_amount)
            if client_reference_id == external_reference:
                preorder = Preorder.query.filter_by(preorder_id=client_reference_id).first()
                book = Book.query.filter_by(book_id=preorder.book_id).first()
                precio_book_01 = book.price
                precio_book_02 = total_paid_amount
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
        else:
            print(f"Request failed with status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

