from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
from models import Member, Book, Reservation

# Blueprintの定義
reservation_bp = Blueprint('reservation', __name__, url_prefix='/reservation')

@reservation_bp.route('/ky01', methods=['GET', 'POST'])
def ky01():
    if request.method == 'POST':
        session['ky_member_number'] = request.form.get('member_number')
        session['ky_title'] = request.form.get('title')
        return redirect(url_for('reservation.ky02'))
    return render_template('ky01.html')

@reservation_bp.route('/ky02')
def ky02():
    member_number = session.get('ky_member_number')
    title = session.get('ky_title', '')
    member = Member.query.filter_by(member_number=member_number).first_or_404()
    books = Book.query.filter(Book.title.contains(title)).all()
    return render_template('ky02.html', books=books, member=member)

@reservation_bp.route('/ky03/<int:book_id>', methods=['GET', 'POST'])
def ky03(book_id):
    member = Member.query.filter_by(member_number=session.get('ky_member_number')).first_or_404()
    book = Book.query.get_or_404(book_id)
    
    if member.member_type == 'student' and book.book_type == 'magazine':
        flash('学生の方は雑誌を予約・貸出できません。')
        return redirect(url_for('reservation.ky02'))

    if request.method == 'POST':
        reservation = Reservation(member_id=member.id, book_id=book.id)
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for('reservation.ky04'))

    return render_template('ky03.html', member=member, book=book)

@reservation_bp.route('/ky04')
def ky04():
    return render_template('ky04.html')