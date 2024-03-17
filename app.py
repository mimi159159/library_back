from functools import wraps
from multiprocessing import allow_connection_pickling
import random
import bcrypt
from flask import Flask, jsonify ,request, send_from_directory, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from flask_restful import Resource, Api
import os,json,time
from flask_cors import CORS,cross_origin
from sqlalchemy.orm import class_mapper
from werkzeug.utils import secure_filename
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError as JWSDecodeError
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError







app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})


db = SQLAlchemy(app)
app.secret_key = 'its_a_secret'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)




# Get the directory where app.py is located
app_directory = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

def allowed_file(filename):
    # print("filename:",filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Define Customer model
class customers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    loans = db.relationship('loans', backref='customers', lazy=True)


# Define Book model
class books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255))
    loans = db.relationship('loans', backref='books', lazy=True)

# Define Loan model
class loans(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    custID = db.Column(db.Integer, ForeignKey('customers.id'))
    bookID = db.Column(db.Integer, ForeignKey('books.id'))
    loandate = db.Column(Date, nullable=False)  
    returndate = db.Column(Date , nullable=True) 


# Define User model with loaded book name
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_name = db.Column(db.String(255),ForeignKey('customers.name'), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    customers = db.relationship('customers', backref='users', lazy=True)


class late_loan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    custID = db.Column(db.Integer, ForeignKey('customers.id'), nullable=False)
    bookID = db.Column(db.Integer, ForeignKey('books.id'), nullable=False)
    loandate = db.Column(Date, nullable=False)
    returndate = db.Column(Date, nullable=False)

@app.route('/')
def hello():
    return "hello"

# Generate a JWT
def generate_token(user_id):
    expiration = int(time.time()) + 7200  # Set the expiration time to 2 hours from the current time
    payload = {'user_id': user_id, 'exp': expiration}
    token = jwt.encode(payload, 'its_a_secret', algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401


        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401


        return f(current_user_id, *args, **kwargs)


    return decorated


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    customer_name = request.form.get("customer_name")

    if not customer_name or not username or not password  :
        return jsonify({'error': 'all fields is required, please fill out all the forms'}), 400

    customer = customers.query.filter(func.lower(customers.name) == func.lower(customer_name)).first()

    # Check if the username is already taken
    existing_user = users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username is already taken'}), 400

    if customer:
        # Hash and salt the password using Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user and add to the database
        new_user = users(username=username, password=hashed_password, customer_name=customer_name, role= role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    
    else:
        return jsonify({'message': "customer not found or does not exist"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # # print( data["username"])
    username = data["username"]
    password = data["password"]
    
    # username = request.form['username']
    # password = request.form['password']
    # Check if the user exists
    user = users.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # Generate an access token with an expiration time
        expires = timedelta(hours=2)
        access_token = create_access_token(identity=user.id, expires_delta=expires, additional_claims={'role': user.role})
        # print(access_token)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'})


@app.route('/uploads/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/allBooks', methods=['GET'] )
def allBooks():
    allBooks = [{"id": book.id,
                 "name": book.name,
                 "author": book.author,
                 "year_published": book.year_published,
                 "type": book.type,
                 'image_path':book.image_path  } for book in books.query.all()]
    # print(allBooks)
    return jsonify(allBooks)


@app.route('/allCust')
def allCust():
    allCust= [{"id":cust.id,
            "name":cust.name,
            "city": cust.city,
            "age":cust.age } for cust in customers.query.all() ]
    
    return jsonify(allCust)

@app.route('/allLoans')
def allLoans():
    allLoans = []

    # Fetch all loan records from the database
    loan_records = loans.query.all()

    for loan in loan_records:
        # Fetch the customer and book details for each loan
        customer = customers.query.get(loan.custID)
        book = books.query.get(loan.bookID)

        # Create a dictionary with loan information including customer and book names
        loan_info = {
            "custID": loan.custID,
            "bookID": loan.bookID,
            "loandate": loan.loandate,
            "returndate": loan.returndate,
            "customer_name": customer.name if customer else "Unknown Customer",
            "book_name": book.name if book else "Unknown Book",
        }

        allLoans.append(loan_info)

    return jsonify(allLoans)


@app.route('/allLateLoan')
def allLateLoan():

    allLateLoan = []

    # Fetch all late loan records from the database
    late_loan_records = late_loan.query.all()

    for late in late_loan_records:
        # Fetch the customer and book details for each late loan using Session.get()
        customer = db.session.get(customers, late.custID)
        book = db.session.get(books, late.bookID)

        # Create a dictionary with late loan information including customer and book names
        late_info = {
            "id": late.id,
            "custID": late.custID,
            "bookID": late.bookID,
            "loandate": late.loandate.strftime('%Y-%m-%d'),  # Format the date as needed
            "returndate": late.returndate.strftime('%Y-%m-%d') if late.returndate else "N/A",  # Format the date or use 'N/A'
            "customer_name": customer.name if customer else "Unknown Customer",
            "book_name": book.name if book else "Unknown Book",
        }

        allLateLoan.append(late_info)

    return jsonify(allLateLoan)


@app.route('/addCust', methods=['POST'])
def addCust():
    name = request.form.get("name")
    city = request.form.get("city")
    age = request.form.get("age")

    if name is None or city is None or age is None:
        return jsonify({'error': "Missing data"}), 400

    new_cust = customers(
        name=name,
        city=city,
        age=age
    )
    db.session.add(new_cust)
 
    db.session.commit()
 

    return jsonify({'msg': "added successfully" })


@app.route('/addBook', methods=['POST'])
@jwt_required()  
def addBook():
    
    # if request.method == 'POST':
      name = request.form.get("name")
      author = request.form.get("author")
      year_published = request.form.get("year_published")
    
    # Generate a random number between 1 and 3 for the 'type' column
      random_type = random.randint(1, 3)
      # Check if a book with the same name and author already exists
      existing_book = books.query.filter(
      func.lower(books.name).ilike(func.lower(name)),
      func.lower(books.author).ilike(func.lower(author))).first()
      if existing_book:
                   return jsonify({'error': "Book already exists"})
    #   if 'image' in request.files:
      image_file= 'uploads/books_DEFAULT.webp'
      image_path = request.files.get('image', None)
    #   print("image_path:", image_path)
      if image_path and allowed_file(image_path.filename):
                # print("inside if")
                # Generate a secure filename and save the image
                filename = secure_filename(image_path.filename)
                # print("filename:", filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                image_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_path.save(image_file)

      new_book = books(
                    name=name,
                      author=author,
                      year_published=year_published,
                      type=random_type,  # Set the 'type' to the generated random number
                      image_path=image_file)
    
      db.session.add(new_book)
      db.session.commit()
    
      return jsonify({'msg': "Book added successfully"})
    

@app.route('/loanBook', methods=['POST'])
@jwt_required() 
def loanBook():
    customer_name = request.form.get("customer")
    customer = customers.query.filter(func.lower(customers.name) == func.lower(customer_name)).first()
    if not customer:
        return jsonify({'error': "Customer not found"})
    book_name = request.form.get("book")
    
    # Find the book by name in a case-insensitive manner and get its ID
    book = books.query.filter(func.lower(books.name) == func.lower(book_name)).first()
    if not book:
        return jsonify({'error': "Book not found"})
    
    # Check if the book is already loaned
    existing_loan = loans.query.filter_by(bookID=book.id, returndate=None).first()
    if existing_loan:
        return jsonify({'error': "Book is already loaned"})
    
    # Create a new loan record with returndate explicitly set to None
    loan_date = datetime.now()
    
    new_loan = loans(
        custID=customer.id,
        bookID=book.id,
        loandate=loan_date,
        returndate=None  # Set returndate to None to indicate the book has not been returned
    )
    
    
    db.session.add(new_loan)
    db.session.commit()
    

    return jsonify({'msg': "Book loaned successfully"})

@app.route('/returnBook', methods=['POST'])
@jwt_required()
def returnBook():
    
    customer_name = request.form.get("customer_name")
    book_name = request.form.get("book_name")
    return_date_str = request.form.get("return_date")

    # Parse the return date string to a datetime object
    # try:
    #     return_date = datetime.strptime(return_date_str, "%Y-%m-%d")
    # except ValueError:
    #     return jsonify({'error': "Invalid return date format. Please use YYYY-MM-DD."})
    return_date = datetime.strptime(return_date_str, "%Y-%m-%d")
    # Find the customer by name
    customer = customers.query.filter(func.lower(customers.name) == func.lower(customer_name)).first()
    if not customer:
        return jsonify({'error': "Customer not found"})

    # Find the book by name
    book = books.query.filter(func.lower(books.name) == func.lower(book_name)).first()
    
    if not book:
        return jsonify({'error': "Book not found"})

    # Check if the book is loaned to the customer
    loan = loans.query.filter(
        (loans.custID == customer.id) & (loans.bookID == book.id) & (loans.returndate.is_(None))
    ).first()

    if not loan:
        return jsonify({'error': "Book is not loaned to the customer"})

    loan.loandate = datetime.combine(loan.loandate, datetime.min.time())

    # Calculate if the return is late based on the book type
    # current_date = datetime.now()
    max_loan_days = {
        1: 10,
        2: 5,
        3: 2
    }
    max_return_date = loan.loandate + timedelta(days=max_loan_days[book.type])
    # print(max_return_date)

    if return_date > max_return_date:
        # print(">>>>>>>>>>>>>>>>>>>> in ")
        # The return is late, create a late loan record
        late = late_loan(
            custID=customer.id,
            bookID=book.id,
            loandate=loan.loandate,
            returndate=return_date
        )
        db.session.add(late)
        loan.returndate = return_date
        db.session.commit()
        # Update the original loan record with the return date
        

        

        # Include a notice that it was a late return in the response
        return jsonify({'msg': "Book returned late! Late loan record created."})

    # Mark the original loan as returned with the return date
    loan.returndate = return_date

    db.session.commit()

    return jsonify({'msg': "Book returned successfully"})


@app.route('/searchCust', methods=['POST'])
def searchCust():
    
    cust_name = request.form.get("cust_name")
   
    cust = customers.query.filter(func.lower(customers.name) == func.lower(cust_name)).first()
    
    if cust:
        found_cust = {
            "id": cust.id,
            "name": cust.name,
            "city":cust.city,
            "age":cust.age    
        }
        return jsonify(found_cust)
    else:
        return jsonify({"error": "customer not found"})


@app.route('/searchBook', methods=['POST'])
def searchBook():
    book_name = request.form.get("book_name")
    
    book = books.query.filter(func.lower(books.name) == func.lower(book_name)).first()
    
    if book:
        found_book = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "year_published": book.year_published,
            "type": book.type,
            "image_path" : book.image_path
        }
        return jsonify(found_book)
    else:
        return jsonify({"error": "Book not found"})

@app.route('/profile')
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    current_user = users.query.get(current_user_id)

    if current_user:
        user_info = {
            "id": current_user.id,
            "customer_name": current_user.customer_name,
            "username": current_user.username,
            "role": current_user.role,
            # "customers_info": []
        }

        # Retrieve customer information for the current user
        cust = customers.query.filter(func.lower(customers.name) == func.lower(current_user.customer_name)).first()

        if cust:
            customer_info = {
                "city": cust.city,
                "age": cust.age,
                # "loans_info": []
            }
            # print(">>>>>>>>>>>>>>>>>>>>>", customer_info)
            # Retrieve loaned books information for the customer
            loans1 = loans.query.filter_by(custID=cust.id).all()

            for loan in loans1:
                book = books.query.get(loan.bookID)
                if book:
                    loan_info = {
                        "book_name": book.name,
                        "loan_date": loan.loandate.strftime("%Y-%m-%d"),
                        "return_date": loan.returndate.strftime("%Y-%m-%d") if loan.returndate else None,
                    }
                    # customer_info["loans_info"].append(loan_info)
            #         print(">>>>>>>>>>>>>>>>>>>>>", customer_info)
            # user_info["customers_info"].append(customer_info)
            # print(">>>>>>>>>>>>>>>>>>>>>", user_info)
        return jsonify(user_info, loan_info, customer_info)
    else:
        return jsonify({"error": "User not found"}), 404



@app.errorhandler(NoAuthorizationError)
@app.errorhandler(ExpiredSignatureError)
@app.errorhandler(InvalidTokenError)
def handle_auth_error(e):
    return jsonify({'error': 'unauthorized', 'message': 'You are not logged in'}), 401


if __name__ == '__main__':
    app.run(debug=True)