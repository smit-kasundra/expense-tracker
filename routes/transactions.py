from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Transaction, Category
from extensions import db
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions')
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('transactions/index.html', transactions=transactions)

@transactions_bp.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add():
    categories = Category.query.filter((Category.user_id == current_user.id) | (Category.is_default == True)).all()
    
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        trans_type = request.form.get('type') # 'income' or 'expense'
        date_str = request.form.get('date')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        description = request.form.get('description')
        payment_method = request.form.get('payment_method')
        category_id = int(request.form.get('category_id'))

        new_tx = Transaction(
            amount=amount, type=trans_type, date=date_obj,
            description=description, payment_method=payment_method,
            category_id=category_id, user_id=current_user.id
        )
        db.session.add(new_tx)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.index'))

    return render_template('transactions/add.html', categories=categories)

@transactions_bp.route('/transactions/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    tx = Transaction.query.get_or_404(id)
    if tx.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('transactions.index'))
        
    db.session.delete(tx)
    db.session.commit()
    flash('Transaction deleted!', 'info')
    return redirect(url_for('transactions.index'))
