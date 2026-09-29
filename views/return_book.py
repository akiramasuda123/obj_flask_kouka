from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_mail import Message
from datetime import date
from extensions import db, mail
from models import Item, Loan, Reservation

return_bp = Blueprint('return_book', __name__, url_prefix='/return')

@return_bp.route('/hk01', methods=['GET', 'POST'])
def hk01():
    if request.method == 'POST':
        m_numbers = [request.form.get(f'management_number_{i}') for i in range(1, 13)]
        session['hk_m_numbers'] = [num for num in m_numbers if num]
        return redirect(url_for('return_book.hk02'))
    return render_template('hk01.html')

@return_bp.route('/hk02', methods=['GET', 'POST'])
def hk02():
    m_numbers = session.get('hk_m_numbers', [])
    items = Item.query.filter(Item.management_number.in_(m_numbers)).all()

    if request.method == 'POST':
        notified_books = []

        for item in items:
            loan = Loan.query.filter_by(item_id=item.id, return_date=None).first()
            if loan:
                loan.return_date = date.today()
            
            item.is_borrowed = False

            reservation = Reservation.query.filter_by(book_id=item.book_id, status='reserved')\
                                           .order_by(Reservation.reserved_at.asc()).first()
            if reservation:
                reservation.status = 'notified'
                notified_books.append(item.book)

                msg = Message(
                    subject='【大原情報科学大学図書館】ご予約図書の取り置き完了のお知らせ',
                    sender='library@oihara.ac.jp',
                    recipients=[reservation.member.email],
                    body=f"{reservation.member.name} 様\n\nご予約いただいた図書「{item.book.title}」が返却されました。\nカウンターに取り置きしております。"
                )
                try:
                    mail.send(msg)
                except Exception as e:
                    print(f"メール送信エラー: {e}")

        db.session.commit()
        return render_template('hk03.html', notified_books=notified_books)

    return render_template('hk02.html', items=items)