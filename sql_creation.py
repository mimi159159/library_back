import sqlite3
from datetime import datetime
con= sqlite3.connect("library.db",check_same_thread=False)

cur=con.cursor()
# Create the 'books' table with the specified columns
cur.execute('''CREATE TABLE books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    author TEXT,
                    year_published INTEGER,
                    type INTEGER,
                    image_path TEXT DEFAULT 'uploads/books_DEFAULT.webp'
                )''')
# Insert sample data into the 'books' table
book_entries = [
    ("To Kill a Mockingbird", "Harper Lee", 1960, 1),
    ("1984", "George Orwell", 1949, 1),
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925, 2),
    ("Pride and Prejudice", "Jane Austen", 1813, 1),
    ("The Hobbit", "J.R.R. Tolkien", 1937, 3),
    ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, 2),
    ("The Catcher in the Rye", "J.D. Salinger", 1951, 2),
    ("Brave New World", "Aldous Huxley", 1932, 3),
    ("The Lord of the Rings", "J.R.R. Tolkien", 1954, 1),
    ("The Hunger Games", "Suzanne Collins", 2008, 3)
]

cur.executemany('''
    INSERT INTO books (name, author, year_published, type)
    VALUES (?, ?, ?, ?)
''', book_entries)

# Create the 'customers' table with the specified columns
cur.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        city TEXT,
        age INTEGER
    )
''')

# Insert sample data into the 'customers' table
customer_data = [
    ("John",  "New York", 30),
    ("Alice",  "Los Angeles", 25),
    ("Robert",  "Chicago", 35),
    ("Mary",  "Houston", 28),
    ("James",  "San Francisco", 40)
]

cur.executemany('''
    INSERT INTO customers (name, city, age)
    VALUES (?,  ?, ?)
''', customer_data)

# Create the 'loans' table with the specified columns
cur.execute('''
    CREATE TABLE loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,    
        custID INTEGER,
        bookID INTEGER,
        loandate DATE,
        returndate DATE,
        FOREIGN KEY (custID) REFERENCES customers(id),
        FOREIGN KEY (bookID) REFERENCES books(id)
    )
''')

# Convert date strings to Unix timestamps
loan_entries = [
    (1, 1, '2024-01-08', '2024-01-18'),  # Type 1: 10 days loan
    (2, 5, '2024-01-09', '2024-01-11'),  # Type 3: 2 days loan
    (3, 3, '2024-01-10', '2024-01-15'),  # Type 2: 5 days loan
    (4, 6, '2024-01-11', '2024-01-16'),  # Type 2: 5 days loan
    (5, 10, '2024-01-12', '2024-01-14')  # Type 3: 2 days loan
]

cur.executemany('''
    INSERT INTO loans (custID, bookID, loandate, returndate)
    VALUES (?, ?, ?, ?)
''', loan_entries)

# Create the 'users' table with the specified columns including 'book_name'
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        customer_name TEXT,
        role TEXT    
    )
''')

# Convert date strings to Unix timestamps and insert sample user data
# user_entries = [
#     ("alice1", "password1", "Alice","user"),
#     ("user2", "password2", "Bob", "The Hobbit", '2024-01-09', '2024-01-14'),
#     ("user3", "password3", "Charlie", "The Great Gatsby", '2024-01-10', '2024-01-12'),
#     ("user4", "password4", "David", "Harry Potter and the Sorcerer's Stone", '2024-01-11', '2024-01-21'),
#     ("user5", "password5", "Eve", "The Hunger Games", '2024-01-12', '2024-01-14')]

# cur.executemany('''
#     INSERT INTO users (username, password, customer_name,role)
#     VALUES (?, ?, ?, ?)
# ''', user_entries)

# Create the 'loanLate' table with the specified columns
cur.execute('''
    CREATE TABLE  late_loan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        custID INTEGER,
        bookID INTEGER,
        loandate DATE,
        returndate DATE,
        FOREIGN KEY (custID) REFERENCES customers(id),
        FOREIGN KEY (bookID) REFERENCES books(id)
    )
''')

# Insert 3 late loan entries into the 'lateLoans' table
late_loan_entries = [
    (1, 1, '2024-01-08', '2024-01-19'),  
    (2, 5, '2024-01-09', '2024-01-16'),  
    (3, 6, '2024-01-11', '2024-01-18')   
]

cur.executemany('''
    INSERT INTO late_loan (custID, bookID, loandate, returndate)
    VALUES (?, ?, ?, ?)
''', late_loan_entries)

con.commit()