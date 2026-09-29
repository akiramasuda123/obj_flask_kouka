from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import date, timedelta
from extensions import db
from models import Member, Item, Loan

loan_bp = Blueprint('loan', __name__, url_prefix='/loan')

@loan_bp.route('/kd01', methods=['GET', 'POST'])
def kd01():
    if request.method == 'POST':
        session['kd_member_number'] = request.form.get('member_number')
        m_numbers = [request.form.get(f'management_number_{i}') for i in range(1, 13)]
        session['kd_m_numbers'] = [num for num in m_numbers if num]
        return redirect(url_for('loan.kd02'))
    return render_template('kd01.html')

@loan_bp.route('/kd02', methods=['GET', 'POST'])
def kd02():
    member = Member.query.filter_by(member_number=session.get('kd_member_number')).first_or_404()
    m_numbers = session.get('kd_m_numbers', [])
    items = Item.query.filter(Item.management_number.in_(m_numbers)).all()

    active_loans_count = Loan.query.filter_by(member_id=member.id, return_date=None).count()

    valid_items = []
    magazine_warnings = []

    for item in items:
        if member.member_type == 'student' and item.book.book_type == 'magazine':
            magazine_warnings.append(item.book)
        else:
            valid_items.append(item)

    remaining_allowance = member.max_loans - (active_loans_count + len(valid_items))

    if request.method == 'POST':
        if remaining_allowance < 0:
            flash('貸出可能上限冊数を超えています。')
            return redirect(url_for('loan.kd01'))

        due_date = date.today() + timedelta(days=21)
        for item in valid_items:
            loan = Loan(member_id=member.id, item_id=item.id, due_date=due_date)
            item.is_borrowed = True
            db.session.add(loan)
        
        db.session.commit()
        session['kd_due_date'] = due_date.strftime('%Y年%m月%d日')
        return redirect(url_for('loan.kd03'))

    return render_template('kd02.html', member=member, valid_items=valid_items, 
                           magazine_warnings=magazine_warnings, remaining_allowance=remaining_allowance)

@loan_bp.route('/kd03')
def kd03():
    due_date = session.get('kd_due_date')
    return render_template('kd03.html', due_date=due_date)