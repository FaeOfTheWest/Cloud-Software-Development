from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

active_users = [
    {
        'id': 1,
        'name': 'Fae Hughes',
        'email': 'fhughes@students.kennesaw.edu'
    }
]

borrowed_books = [
    {
        'id': 1,
        'currentHolder': 1,
        'bookTitle': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'borrowDate': '08/01/2023',
        'dueDate': '11/01/2023'
    },
    {
        'id': 2,
        'currentHolder': None,
        'bookTitle': '1984',
        'author': 'George Orwell',
        'borrowDate': None,
        'dueDate': None
    },
    {
        'id': 3,
        'currentHolder': None,
        'bookTitle': 'Journal #3',
        'author': 'Alex Hirsch',
        'borrowDate': None,
        'dueDate': None
    },
    {
        'id': 4,
        'currentHolder': 1,
        'bookTitle': 'The Hobbit',
        'author': 'J.R.R. Tolkien',
        'borrowDate': "10/3/2026",
        'dueDate': "11/3/2026"
    }
]



@app.route('/api/users', methods=['GET'])
def get_users():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({
        'success': True,
        'data': active_users,
        'timestamp': timestamp
    })


@app.route('/api/books', methods=['GET'])
def get_books():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({
        'success': True,
        'data': borrowed_books,
        'timestamp': timestamp
    })


@app.route('/api/books/available', methods=['GET'])
def get_available_books():
    """Get only books that are available (not borrowed)"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    available = [book for book in borrowed_books 
                 if book['currentHolder'] is None]
    return jsonify({
        'success': True,
        'data': available,
        'timestamp': timestamp
    })


@app.route('/api/users/<int:user_id>/books', methods=['GET'])
def get_user_books(user_id):
    """Get all books currently borrowed by a specific user"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_books = [book for book in borrowed_books 
                  if book['currentHolder'] == user_id]
    
    # Check if user exists
    user = next((u for u in active_users if u['id'] == user_id), None)
    if not user:
        return jsonify({
            'success': False,
            'message': 'User not found',
            'timestamp': timestamp
        }), 404
    
    return jsonify({
        'success': True,
        'userName': user['name'],
        'data': user_books,
        'timestamp': timestamp
    })


@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({
            'success': False,
            'message': 'Name and email required',
            'timestamp': timestamp
        }), 400

    new_user = {
        'id': max([u['id'] for u in active_users]) + 1
            if active_users else 1,
        'name': data['name'],
        'email': data['email']
    }

    active_users.append(new_user)

    return jsonify({
        'success': True,
        'data': new_user,
        'message': 'User added',
        'timestamp': timestamp
    }), 201

#deprecated add books
# @app.route('/api/books', methods=['POST'])
# def add_book():
#     data = request.get_json()
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     if not data or not data.get('bookTitle'):
#         return jsonify({
#             'success': False,
#             'message': 'All fields required',
#             'timestamp': timestamp
#         }), 400
    
#     # Allow currentHolder to be optional (None if not provided)
#     current_holder = data.get('currentHolder')
    
#     new_book = {
#         'id': max([b['id'] for b in borrowed_books]) + 1
#             if borrowed_books else 1,
#         'currentHolder': current_holder,
#         'bookTitle': data['bookTitle'],
#         'author': data.get('author', 'Unknown'),
#         'borrowDate': datetime.now().strftime('%Y-%m-%d') 
#             if current_holder else None,
#         'dueDate': data['dueDate'] if current_holder else None
#     }

#     borrowed_books.append(new_book)

#     return jsonify({
#         'success': True,
#         'data': new_book,
#         'message': 'Book added',
#         'timestamp': timestamp
#     }), 201


@app.route('/api/books/borrow', methods=['POST'])
def borrow_book():
    """Mark a book as borrowed by a user"""
    data = request.get_json()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not data or not data.get('bookId') or not data.get('userId') \
       or not data.get('dueDate'):
        return jsonify({
            'success': False,
            'message': 'bookId, userId, and dueDate required',
            'timestamp': timestamp
        }), 400
    
    book_id = data['bookId']
    user_id = data['userId']
    due_date = data['dueDate']
    
    # Find the book
    book = next((b for b in borrowed_books if b['id'] == book_id), None)
    if not book:
        return jsonify({
            'success': False,
            'message': 'Book not found',
            'timestamp': timestamp
        }), 404
    
    # Check if book is already borrowed
    if book['currentHolder'] is not None:
        holder = next((u for u in active_users 
                      if u['id'] == book['currentHolder']), None)
        holder_name = holder['name'] if holder else 'Unknown'
        return jsonify({
            'success': False,
            'message': f'Book already borrowed by {holder_name}',
            'timestamp': timestamp
        }), 400
    
    # Check if user exists
    user = next((u for u in active_users if u['id'] == user_id), None)
    if not user:
        return jsonify({
            'success': False,
            'message': 'User not found',
            'timestamp': timestamp
        }), 404
    
    # Update the book
    book['currentHolder'] = user_id
    book['borrowDate'] = datetime.now().strftime('%Y-%m-%d')
    book['dueDate'] = due_date
    
    return jsonify({
        'success': True,
        'data': book,
        'message': f'{user["name"]} borrowed {book["bookTitle"]}',
        'timestamp': timestamp
    }), 201

@app.route('/api/books/add', methods=['POST'])
def add_book_to_library():
    """Add a new book to the library"""
    data = request.get_json()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not data or not data.get('bookTitle') or not data.get('author'):
        return jsonify({
            'success': False,
            'message': 'bookTitle and author required',
            'timestamp': timestamp
        }), 400
    
    new_book = {
        'id': max([b['id'] for b in borrowed_books]) + 1 
            if borrowed_books else 1,
        'currentHolder': None,  # New books start as available
        'bookTitle': data['bookTitle'],
        'author': data['author'],
        'borrowDate': None,
        'dueDate': None
    }
    
    borrowed_books.append(new_book)
    
    return jsonify({
        'success': True,
        'data': new_book,
        'message': 'Book added to library',
        'timestamp': timestamp
    }), 201

@app.route('/api/books/return', methods=['POST'])
def return_book():
    """Mark a book as returned (no longer borrowed)"""
    data = request.get_json()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not data or not data.get('bookId'):
        return jsonify({
            'success': False,
            'message': 'bookId required',
            'timestamp': timestamp
        }), 400
    
    book_id = data['bookId']
    
    # Find the book
    book = next((b for b in borrowed_books if b['id'] == book_id), None)
    if not book:
        return jsonify({
            'success': False,
            'message': 'Book not found',
            'timestamp': timestamp
        }), 404
    
    # Check if book is actually borrowed
    if book['currentHolder'] is None:
        return jsonify({
            'success': False,
            'message': 'This book is not currently borrowed',
            'timestamp': timestamp
        }), 400
    
    # Get the user who had it
    user = next((u for u in active_users 
                if u['id'] == book['currentHolder']), None)
    user_name = user['name'] if user else 'Unknown'
    
    # Return the book
    book['currentHolder'] = None
    book['borrowDate'] = None
    book['dueDate'] = None
    
    return jsonify({
        'success': True,
        'data': book,
        'message': f'{user_name} returned {book["bookTitle"]}',
        'timestamp': timestamp
    }), 200


@app.route('/health', methods=['GET'])
def health():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({
        'status': 'healthy',
        'timestamp': timestamp
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)