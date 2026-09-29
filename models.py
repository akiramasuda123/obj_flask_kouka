from extensions import db
from datetime import datetime, date

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    member_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    member_type = db.Column(db.String(10), nullable=False) # 'student' or 'staff'

    @property
    def max_loans(self):
        return 6 if self.member_type == 'student' else 12


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    book_type = db.Column(db.String(10), nullable=False) # 'book' or 'magazine'


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    management_number = db.Column(db.String(20), unique=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    is_borrowed = db.Column(db.Boolean, default=False)
    
    book = db.relationship('Book', backref=db.backref('items', lazy=True))


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='reserved') # reserved, notified, completed, canceled

    member = db.relationship('Member', backref=db.backref('reservations', lazy=True))
    book = db.relationship('Book', backref=db.backref('reservations', lazy=True))


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    loan_date = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

    member = db.relationship('Member', backref=db.backref('loans', lazy=True))
    item = db.relationship('Item', backref=db.backref('items', lazy=True))