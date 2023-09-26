from app.extensions import db

# Define the Authors table
class Author(db.Model):
    __tablename__ = 'authors'
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String)
    author_lastname = db.Column(db.String)
    # Add other author information columns as needed

# Define the Books table
class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    isbn = db.Column(db.String)
    publication_date = db.Column(db.DateTime)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    genre = db.relationship("Genre")  # Create a relationship with the Genre table
    price = db.Column(db.Float)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.currency_id'))
    currency = db.relationship("Currency")  # Create a relationship with the Currency table
    publisher = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    author = db.relationship("Author")  # Create a relationship with the Authors table
    # Add other book-related information columns as needed

# Define the Customers table
class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    # Add other customer information columns as needed

# Define the PaymentMethods table
class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # Add other payment method information columns as needed

# Define the Orders table
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    customer = db.relationship("Customer")  # Create a relationship with the Customers table
    order_date = db.Column(db.DateTime)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    payment_method = db.relationship("PaymentMethod")  # Create a relationship with the PaymentMethods table
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.status_id'))
    status = db.relationship("Status")  # Create a relationship with the Status table
    transfer_id = db.Column(db.String)
    # Add other order-related information columns as needed

# Define the OrderItems table
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    order = db.relationship("Order")  # Create a relationship with the Orders table
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    book = db.relationship("Book")  # Create a relationship with the Books table
    quantity = db.Column(db.Integer)
    discount = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    # Add other order item-related information columns as needed

# Define the Preorders table
class Preorder(db.Model):
    __tablename__ = 'preorders'
    preorder_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    customer = db.relationship("Customer")  # Create a relationship with the Customers table
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    book = db.relationship("Book")  # Create a relationship with the Books table
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    payment_method = db.relationship("PaymentMethod")  # Create a relationship with the PaymentMethods table
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.status_id'))
    status = db.relationship("Status")  # Create a relationship with the Status table
    # Add other preorder-related information columns as needed

class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String)
    # Add other genre-related information columns as needed

# Define the Currency table
class Currency(db.Model):
    __tablename__ = 'currencies'
    currency_id = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String)
    # Add other currency-related information columns as needed

# Define the Status table
class Status(db.Model):
    __tablename__ = 'statuses'
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String)
    # Add other status-related information columns as needed

class Contacto(db.Model):
    __tablename__ = 'contacto'
    contact_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    name = db.Column(db.String)
    message = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
