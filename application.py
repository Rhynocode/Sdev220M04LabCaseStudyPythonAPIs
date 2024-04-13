#Ryan Hayes
#Sdev220
#M04 Lab - Case Study: Python APIs
#Program provides a basic API for adding, removing, and updating books in a database
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy part of the app, specifying the database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an SQLAlchemy object by passing it the application
db = SQLAlchemy(app)

# Define a Book model/class that will be used to create and query database records
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    # This method returns a string representation of the object, useful for debugging
    def __repr__(self):
        return f'<Book {self.title}>'

    # This method converts the book object into a dictionary, useful for JSON responses
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher
        }

# API endpoint to manage books (add new books or fetch all books)
@app.route('/api/books', methods=['POST', 'GET'])
def manage_books():
    if request.method == 'POST':
        data = request.get_json()  # Get data sent with POST request
        new_book = Book(title=data['title'], author=data['author'], publisher=data['publisher'])
        db.session.add(new_book)  # Add new book to the database session
        db.session.commit()  # Commit the session to save the book to the database
        return jsonify(new_book.to_dict()), 201  # Return the added book's data as JSON with status 201

    books = Book.query.all()  # Fetch all books if method is GET
    return jsonify([book.to_dict() for book in books])  # Return a list of books as JSON

# API endpoint to fetch, update or delete a book by its ID
@app.route('/api/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_by_id(book_id):
    book = Book.query.get_or_404(book_id)  # Fetch the book by ID or return 404 if not found
    if request.method == 'GET':
        return jsonify(book.to_dict())  # Return the book's data as JSON

    if request.method == 'PUT':
        data = request.get_json()  # Get data sent with PUT request
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.publisher = data.get('publisher', book.publisher)
        db.session.commit()
        return jsonify(book.to_dict()), 200  # Return the updated book's data as JSON

    db.session.delete(book)  # Delete the book from the database session
    db.session.commit()  # Commit the session to apply the changes
    return '', 204  # Return an empty response with status 204 (no content)

# Check if the script is executed as the main program and not imported as a module
if __name__ == '__main__':
    db.create_all()  # Create database tables based on the models defined
    app.run(debug=True)  # Run the application with debugging enabled
