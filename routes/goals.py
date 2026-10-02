from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import FinancialGoal
from extensions import db
from datetime import datetime

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/goals')
@login_required
def index():
    goals = FinancialGoal.query.filter_by(user_id=current_user.id).all()
    goal_data = []
    for g in goals:
        progress = (g.current_amount / g.target_amount) * 100 if g.target_amount > 0 else 0
        goal_data.append({'goal': g, 'progress': round(progress, 2)})
    return render_template('goals/index.html', goal_data=goal_data)

@goals_bp.route('/goals/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        target = float(request.form.get('target_amount'))
        current = float(request.form.get('current_amount', 0))
        deadline_str = request.form.get('deadline')
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None

        new_goal = FinancialGoal(
            name=name, target_amount=target, current_amount=current,
            deadline=deadline, user_id=current_user.id
        )
        db.session.add(new_goal)
        db.session.commit()
        flash('Financial goal added!', 'success')
        return redirect(url_for('goals.index'))

    return render_template('goals/add.html')

@goals_bp.route('/goals/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    g = FinancialGoal.query.get_or_404(id)
    if g.user_id == current_user.id:
        add_amount = float(request.form.get('add_amount', 0))
        g.current_amount += add_amount
        db.session.commit()
        flash('Goal progress updated!', 'success')
    return redirect(url_for('goals.index'))
