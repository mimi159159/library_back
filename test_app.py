# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# import unittest
# from app import   app,db, customers, users, books, loans, late_loan
# import json
# # from sql_test import app as test_app 



# app = Flask(__name__)



# # Configure JWT settings (if you are using JWT for authentication)
# app.config['JWT_SECRET_KEY'] = 'your-secret-key'
# jwt = JWTManager(app)
# # Configure the SQLAlchemy database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # Initialize the SQLAlchemy database
# # db = SQLAlchemy(app)
# class TestApp(unittest.TestCase):


#     @classmethod
#     def setUpClass(cls):
#         # Use the Flask app and SQLAlchemy instance from app.py
#         cls.app = app
#         cls.client = app.test_client()

#         # Create the database tables within a test context
#         db.init_app(app)
#         with cls.app.app_context():
#             db.create_all()

#     @classmethod
#     def tearDownClass(cls):
#         # Drop the database tables after all tests are done
#         with cls.app.app_context():
#             db.drop_all()


#     def register_user(self, username, password, role, customer_name):
#         return self.client.post('/register', data={
#             'username': username,
#             'password': password,
#             'role': role,
#             'customer_name': customer_name
#         })

#     def login_user(self, username, password):
#         return self.app.post('/login', json={
#             'username': username,
#             'password': password
#         })

#     # Test the registration route
#     def test_register(self):
#         response =self.register_user('testuser', 'testpassword', 'user', 'Test Customer')
#         self.assertEqual(response.status_code, 201)
#         self.assertIn(b'User created successfully', response.data)

#     # # Test the login route
#     # def test_login(self):
#     #     self.register_user('testuser', 'testpassword', 'user', 'Test Customer')
#     #     response = self.login_user('testuser', 'testpassword')
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn(b'access_token', response.data)

#     # # Add more test cases for other routes and functions as needed

#     # def test_allBooks_route(self):
#     #     with self.app:
#     #         with self.app.app_context():
#     #             # Add sample books to the database for testing
#     #             book1 = books(name="Book 1", author="Author 1", year_published=2020, type=1)
#     #             book2 = books(name="Book 2", author="Author 2", year_published=2021, type=2)
#     #             db.session.add_all([book1, book2])
#     #             db.session.commit()

#     #         # Send a GET request to the /allBooks route
#     #         response = self.app.get('/allBooks')
#     #         data = response.get_json()

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(len(data), 2)

#     # def test_allCust_route(self):
#     #     # Add sample customers to the database for testing
#     #     customer1 = customers(name="Customer 1", city="City 1", age=30)
#     #     customer2 = customers(name="Customer 2", city="City 2", age=25)
#     #     db.session.add_all([customer1, customer2])
#     #     db.session.commit()

#     #     # Send a GET request to the /allCust route
#     #     response = self.app.get('/allCust')
#     #     data = response.get_json()

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(len(data), 2)  # Check if the correct number of customers is returned

#     # def test_allLoans_route(self):
#     #     # Add sample loans to the database for testing
#     #     customer = customers(name="Customer", city="City", age=30)
#     #     book1 = books(name="Book 1", author="Author 1", year_published=2020, type=1)
#     #     book2 = books(name="Book 2", author="Author 2", year_published=2021, type=2)
#     #     loan1 = loans(custID=customer.id, bookID=book1.id, loandate="2022-01-01")
#     #     loan2 = loans(custID=customer.id, bookID=book2.id, loandate="2022-01-02")
#     #     db.session.add_all([customer, book1, book2, loan1, loan2])
#     #     db.session.commit()

#     #     # Send a GET request to the /allLoans route
#     #     response = self.app.get('/allLoans')
#     #     data = response.get_json()

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(len(data), 2)  # Check if the correct number of loans is returned

#     # def test_allLateLoan_route(self):
#     #     # Add sample late loans to the database for testing
#     #     customer = customers(name="Customer", city="City", age=30)
#     #     book1 = books(name="Book 1", author="Author 1", year_published=2020, type=1)
#     #     book2 = books(name="Book 2", author="Author 2", year_published=2021, type=2)
#     #     late1 = late_loan(custID=customer.id, bookID=book1.id, loandate="2022-01-01", returndate="2022-01-12")
#     #     late2 = late_loan(custID=customer.id, bookID=book2.id, loandate="2022-01-02", returndate="2022-01-15")
#     #     db.session.add_all([customer, book1, book2, late1, late2])
#     #     db.session.commit()

#     #     # Send a GET request to the /allLateLoan route
#     #     response = self.app.get('/allLateLoan')
#     #     data = response.get_json()

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(len(data), 2)  # Check if the correct number of late loans is returned



#     # def get_access_token(self):
#     #     response = self.client.post('/login', json={
#     #         'username': 'testuser',
#     #         'password': 'testpassword'
#     #     })
#     #     data = json.loads(response.data)
#     #     return data['access_token']

#     # # Test the /addCust route
#     # def test_add_customer(self):
#     #     # First, log in with a user who has the 'Admin' role to access this route
#     #     self.app.post('/register', data={
#     #         'username': 'testadmin',
#     #         'password': 'adminpassword',
#     #         'role': 'Admin',
#     #         'customer_name': 'Test Admin Customer'
#     #     })

#     #     admin_token = self.get_access_token()

#     #     # Now, use the admin token to add a customer
#     #     response = self.app.post('/addCust', data={
#     #         'name': 'Test Customer',
#     #         'city': 'Test City',
#     #         'age': 30
#     #     }, headers={'Authorization': f'Bearer {admin_token}'})

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn(b'added successfully', response.data)

#     # # Test the /addBook route
#     # def test_add_book(self):
#     #     # First, log in with a user who has the 'Admin' role to access this route
#     #     self.app.post('/register', data={
#     #         'username': 'testadmin',
#     #         'password': 'adminpassword',
#     #         'role': 'Admin',
#     #         'customer_name': 'Test Admin Customer'
#     #     })

#     #     admin_token = self.get_access_token()

#     #     # Now, use the admin token to add a book
#     #     response = self.app.post('/addBook', data={
#     #         'name': 'Test Book',
#     #         'author': 'Test Author',
#     #         'year_published': 2022
#     #     }, headers={'Authorization': f'Bearer {admin_token}'})

#     #     self.assertEqual(response.status_code, 200)   


#     # def test_loan_book(self):
#     #     # First, log in with a user who has the 'User' role to access this route
#     #     self.app.post('/register', data={
#     #         'username': 'testuser',
#     #         'password': 'testpassword',
#     #         'role': 'User',
#     #         'customer_name': 'Test Customer'
#     #     })

#     #     user_token = self.get_access_token()

#     #     # Create a customer and a book in the test database
#     #     response = self.app.post('/addCust', data={
#     #         'name': 'Test Customer',
#     #         'city': 'Test City',
#     #         'age': 30
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)

#     #     response = self.app.post('/addBook', data={
#     #         'name': 'Test Book',
#     #         'author': 'Test Author',
#     #         'year_published': 2022
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)

#     #     # Use the user token to loan the book
#     #     response = self.app.post('/loanBook', data={
#     #         'customer': 'Test Customer',
#     #         'book': 'Test Book'
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn(b'Book loaned successfully', response.data)

#     # # Test the /returnBook route
#     # def test_return_book(self):
#     #     # First, log in with a user who has the 'User' role to access this route
#     #     self.app.post('/register', data={
#     #         'username': 'testuser',
#     #         'password': 'testpassword',
#     #         'role': 'User',
#     #         'customer_name': 'Test Customer'
#     #     })

#     #     user_token = self.get_access_token()

#     #     # Create a customer, a book, and loan the book in the test database
#     #     response = self.app.post('/addCust', data={
#     #         'name': 'Test Customer',
#     #         'city': 'Test City',
#     #         'age': 30
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)

#     #     response = self.app.post('/addBook', data={
#     #         'name': 'Test Book',
#     #         'author': 'Test Author',
#     #         'year_published': 2022
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)

#     #     response = self.app.post('/loanBook', data={
#     #         'customer': 'Test Customer',
#     #         'book': 'Test Book'
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)

#     #     # Use the user token to return the book
#     #     response = self.app.post('/returnBook', data={
#     #         'customer_name': 'Test Customer',
#     #         'book_name': 'Test Book',
#     #         'return_date': '2023-01-15'  # Replace with a valid return date
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn(b'Book returned successfully', response.data) 


#     # def test_search_customer(self):
#     #     # First, log in with a user who has the 'User' role to access this route
#     #     self.app.post('/register', data={
#     #         'username': 'testuser',
#     #         'password': 'testpassword',
#     #         'role': 'User',
#     #         'customer_name': 'Test Customer'
#     #     })

#     #     user_token = self.get_access_token()

#     #     # Create a customer in the test database
#     #     response = self.app.post('/addCust', data={
#     #         'name': 'Test Customer',
#     #         'city': 'Test City',
#     #         'age': 30
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)

#     #     # Use the user token to search for the customer
#     #     response = self.app.post('/searchCust', data={
#     #         'cust_name': 'Test Customer'
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn(b'Test Customer', response.data)  # Check if the customer is found

#     # # Test the /searchBook route
#     # def test_search_book(self):
#     #     # First, log in with a user who has the 'User' role to access this route
#     #     self.app.post('/register', data={
#     #         'username': 'testuser',
#     #         'password': 'testpassword',
#     #         'role': 'User',
#     #         'customer_name': 'Test Customer'
#     #     })

#     #     user_token = self.get_access_token()

#     #     # Create a book in the test database
#     #     response = self.app.post('/addBook', data={
#     #         'name': 'Test Book',
#     #         'author': 'Test Author',
#     #         'year_published': 2022
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)

#     #     # Use the user token to search for the book
#     #     response = self.app.post('/searchBook', data={
#     #         'book_name': 'Test Book'
#     #     }, headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn(b'Test Book', response.data)  # Check if the book is found

#     # # Test the /profile route
#     # def test_profile(self):
#     #     # First, log in with a user who has the 'User' role to access this route
#     #     self.app.post('/register', data={
#     #         'username': 'testuser',
#     #         'password': 'testpassword',
#     #         'role': 'User',
#     #         'customer_name': 'Test Customer'
#     #     })

#     #     user_token = self.get_access_token()

#     #     # Use the user token to access the profile route
#     #     response = self.app.get('/profile', headers={'Authorization': f'Bearer {user_token}'})

#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn(b'Test Customer', response.data)  # Check if the user's profile is returned            
# if __name__ == '__main__':
#     unittest.main()
