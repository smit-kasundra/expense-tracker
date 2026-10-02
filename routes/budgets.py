from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Budget, Category, Transaction
from extensions import db
from datetime import datetime
from sqlalchemy import func

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/budgets')
@login_required
def index():
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    
    budget_data = []
    for budget in budgets:
        spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.category_id == budget.category_id,
            Transaction.type == 'expense',
            db.extract('month', Transaction.date) == budget.month,
            db.extract('year', Transaction.date) == budget.year
        ).scalar() or 0.0
        
        remaining = budget.amount - spent
        percent_used = (spent / budget.amount) * 100 if budget.amount > 0 else 0
        
        budget_data.append({
            'budget': budget,
            'spent': spent,
            'remaining': remaining,
            'percent_used': round(percent_used, 2)
        })

    return render_template('budgets/index.html', budget_data=budget_data)

@budgets_bp.route('/budgets/add', methods=['GET', 'POST'])
@login_required
def add():
    categories = Category.query.filter(
        (Category.type == 'expense') & 
        ((Category.user_id == current_user.id) | (Category.is_default == True))
    ).all()
    
    if request.method == 'POST':
        category_id = int(request.form.get('category_id'))
        amount = float(request.form.get('amount'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))

        existing = Budget.query.filter_by(
            user_id=current_user.id, category_id=category_id, month=month, year=year
        ).first()

        if existing:
            existing.amount = amount
            flash('Budget updated!', 'success')
        else:
            new_budget = Budget(
                amount=amount, month=month, year=year,
                category_id=category_id, user_id=current_user.id
            )
            db.session.add(new_budget)
            flash('Budget created successfully!', 'success')
            
        db.session.commit()
        return redirect(url_for('budgets.index'))

    return render_template('budgets/add.html', categories=categories)

@budgets_bp.route('/budgets/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    b = Budget.query.get_or_404(id)
    if b.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
    else:
        db.session.delete(b)
        db.session.commit()
        flash('Budget deleted.', 'info')
    return redirect(url_for('budgets.index'))
