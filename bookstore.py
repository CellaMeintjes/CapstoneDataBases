# CAPSTONE PROJECT - DATABASES

# -------- MODULES --------------
import sqlite3
from prettytable import PrettyTable

# Specify the absolute path to the directory and the database file
db_path = 'c:/Users/mloui/Dropbox/MM23060008708/2 - Introduction to Software Engineering/L2T12 - SQLite/python_programming_db'


# Connect to database
def connect_to_database():
    db = sqlite3.connect(db_path)
    cursor = db.cursor()  # Creata cursor object
    return db, cursor


# SQL functions
def create_table():
    db, cursor = connect_to_database()
    sql_table = '''
CREATE TABLE IF NOT EXISTS book(
id INTEGER PRIMARY KEY,
title VARCHAR,
author VARCHAR,
qty INTEGER
)'''
    cursor.execute(sql_table)
    db.commit()
    close_database(db)


def retrieve_data():
    db, cursor = connect_to_database()
    # Retrieve data with SQL command
    retrieve_sql = 'SELECT * FROM book'
    cursor.execute(retrieve_sql)
    data = cursor.fetchall()

    # Create table structure and add data from ebookstore
    table = PrettyTable()
    table.field_names = ["ID", "Title", "Author", "Quantity"]

    for row in data:
        table.add_row(row)

    print(table)

    close_database(db)


def close_database(db):
    db.close()


# Function to print heading lines
def print_heading(heading):
    print('-' * 50)
    print(heading)
    print('-' * 50)


# Function to enter new book
def enter_book():
    print_heading('Add new book')

    id = input('Enter the id of the book: \n')
    title = input('Enter the title of the book:\n')
    author = input('Enter the author of the book: \n')
    qty = input('Enter the quantity: \n')

    db, cursor = connect_to_database()

    try:
        cursor.execute('''INSERT INTO book(id, title, author, qty)
                   VALUES (?, ?, ?, ?) 
                   ''', (id, title, author, qty))
        db.commit()

        print('New book has been added to the database.')
        close_database(db)
    except sqlite3.Error as e:
        print('Error:', e)


# Function to update book
def update_book():
    print_heading('Update book')

    id = input('Enter the id of the book you would like to update: \n')

    # Check if the book exists in the database
    db, cursor = connect_to_database()
    cursor.execute('''SELECT title, author, qty FROM book WHERE id = ?''', (id,))
    book_details = cursor.fetchone()
    if book_details:
        print('Current Book Details:')
        print('Title: ', book_details[0])
        print('Author: ', book_details[1])
        print('Quatntity: ', book_details[2])

        # Prompt user option for book that needs to updated
        Update_option = input('''Select from the option below. Only type the letter.
                            1 - Title
                            2 - Author
                            3 - Quantity
                            0 - Return to main menu ''')

        if Update_option == '1':
            # Update title on ebookstore
            updated_title = input('Enter the update title: \n')
            cursor.execute("UPDATE book SET title = ? WHERE id = ?", (updated_title, id))
            db.commit()
            print('Title has been updated\n')

        elif Update_option == '2':
            # Update title on ebookstore
            updated_author = input('Enter the updated author information: \n')
            cursor.execute("UPDATE book SET author = ? WHERE id = ?", (updated_author, id))
            db.commit()
            print('Author has been updated.\n')

        elif Update_option == '3':
            # Update title on ebookstore
            update_qty = input('Enter the updated quantity: \n')
            update_qty = int(update_qty)
            cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (update_qty, id))
            db.commit()
            print('Quantity has been updated.\n')

        elif Update_option == '0':
            menu_options()

        else:
            print('You have entered an invalid option. Please try again\n')
            Update_option = input('''Select from the option below. Only type the letter.
                            1 - Title
                            2 - Author
                            3 - Quantity ''')
    else:
        print('book with ID {} not found.'.format(id))

    print('Book with Id {} successfully updated!'.format(id))
    close_database(db)


# Function to delete book
def delete_book():
    print_heading('Delete book')

    id = input('Enter the id of the book you would like to remove: \n')
    id = int(id)  # Casting id to int

    # Connect to ebookstore
    db, cursor = connect_to_database()

    # Check if the book exists
    cursor.execute('''SELECT title, author FROM book WHERE id = ?  ''', (id,))
    book_data = cursor.fetchone()

    if book_data:
        title, author = book_data
        cursor.execute('''DELETE FROM book WHERE id = ? AND author = ? ''', (id, author,))
        print('Book "{}" by {} has been removed.'.format(title, author))
        db.commit()

    # If book is not found in ebookstore
    else:
        print('Book with id {} not found'.format(id))

    # Close the database connection
    close_database(db)


# Function to search book
def search_book():
    print_heading('Search book')

    search_option = input('''How would you like to search?
                          Select from the option below. Only type the letter.
                          1 - Id
                          2 - Title
                          3 - Author
                          0 - Menu''')
    db, cursor = connect_to_database()

    if search_option == '1':
        id = input('Enter id of the book you are searching for: \n')
        id = int(id)
        cursor.execute("SELECT * FROM book WHERE id = ?", (id,))
        data = cursor.fetchall()
        if data:
            print('Found {} book(s) with ID {}:'.format(len(data), id))
            for row in data:
                print('ID: {}, Title: {}, Author: {}, Quantity: {}'.format(row[0], row[1], row[2], row[3]))
        else:
            print('No books found with ID {}.'.format(id))

    elif search_option == '2':
        title = input('Enter the title of the book you are searching for: \n')
        cursor.execute("SELECT * FROM book WHERE title LIKE ?", ('%' + title + '%',))
        data = cursor.fetchall()
        if data:
            print('Found {} book(s) with title containing "{}":'.format(len(data), title))
            for row in data:
                print('ID: {}, Title: {}, Author: {}, Quantity: {}'.format(row[0], row[1], row[2], row[3]))
        else:
            print('No books found with title containing "{}".'.format(title))

    elif search_option == '3':
        author = input('Enter the author of the book you are searching for: \n')
        cursor.execute("SELECT * FROM book WHERE author LIKE ?", ('%' + author + '%',))
        data = cursor.fetchall()
        if data:
            print('Found {} book(s) by author "{}":'.format(len(data), author))
            for row in data:
                print('ID: {}, Title: {}, Author: {}, Quantity: {}'.format(row[0], row[1], row[2], row[3]))
        else:
            print('No books found by author "{}".'.format(author))

    elif search_option == "0":
        menu_options()

    else:
        print('Invalid input. Plese try again')
        search_option = input('''How would you like to search?
                          Select from the option below. Only type the letter.
                          1 - Id
                          2 - Title
                          3 - Author
                          0 - Menu''')
    close_database(db)


create_table()


# function to display menu option
def menu_options():
    print('''Select an option from the menu below:
                 1 - Enter book
                 2 - Update book
                 3 - Delete book
                 4 - Search books
                 5 - Display Inventory
                 0 - Exit \n''')

# I added one more option in the menu to display inventory so that the clerk could see the all the 
# books available in the ebookstore'''


# Display menu options
print_heading('Welcome to E-bookstore!')


menu_options()
option = input('Enter your option from the menu:\n')


while option != '0':
    if option == '1':
        # Enter new book
        enter_book()

    elif option == '2':
        # Update a book
        update_book()

    elif option == '3':
        # Delete/ remove a book
        delete_book()

    elif option == '4':
        # Search for a book
        search_book()

    elif option == '5':
        # Display inventory
        retrieve_data()

    else:
        print('!' * 10)
        print('Invalid option. Please try again')

    print('')
    menu_options()
    option = input('Enter you option from the menu:\n')

print('Thank you for using this program. Goodbye!')

# SOURCES USED:
# https://www.tutorialspoint.com/printing-lists-as-tabular-data-in-python#:~:text=We%20import%20the%20PrettyTable%20class,automatically%20in%20a%20tabular%20format. 
# https://pypi.org/project/prettytable/
# https://www.tutorialspoint.com/sqlite/sqlite_delete_query.htm
# https://www.tutorialspoint.com/sqlite/sqlite_update_query.htm 
# https://www.tutorialspoint.com/sqlite/sqlite_insert_query.htm
