from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Transaction, Budget
from extensions import db
from sqlalchemy import func
import pandas as pd
import json
import plotly.express as px
import plotly.utils
from utils.data_processing import get_transactions_df
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Calculate basic totals
    total_income = db.session.query(func.sum(Transaction.amount)).filter_by(
        user_id=current_user.id, type='income'
    ).scalar() or 0.0
    
    total_expense = db.session.query(func.sum(Transaction.amount)).filter_by(
        user_id=current_user.id, type='expense'
    ).scalar() or 0.0
    
    current_balance = total_income - total_expense

    # Get recent transactions
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).limit(5).all()
        
    df = get_transactions_df(current_user.id)
    
    chart_json_1 = None
    chart_json_2 = None
    highest_category = "N/A"
    insights = []
    
    if not df.empty:
        # Highest Expense Category this month
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        
        expenses_df = df[df['type'] == 'expense']
        if not expenses_df.empty:
            category_totals = expenses_df.groupby('category')['amount'].sum().reset_index()
            if not category_totals.empty:
                highest_cat_row = category_totals.loc[category_totals['amount'].idxmax()]
                highest_category = f"{highest_cat_row['category']} (₹{highest_cat_row['amount']:.2f})"
                
            # Chart 1: Category-wise Expense (Pie Chart)
            fig1 = px.pie(category_totals, values='amount', names='category', title="Expense by Category")
            chart_json_1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Chart 2: Income vs Expense Over Time (Bar/Line Chart)
        monthly_summary = df.groupby([df['date'].dt.to_period('M'), 'type'])['amount'].sum().reset_index()
        monthly_summary['date'] = monthly_summary['date'].dt.to_timestamp()
        
        if not monthly_summary.empty:
            fig2 = px.bar(monthly_summary, x='date', y='amount', color='type', barmode='group', title="Income vs Expense Trend")
            chart_json_2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        # Rule-based Insight Example
        insights.append(f"You have recorded {len(df)} transactions so far.")
        if highest_category != "N/A":
            insights.append(f"Your highest spending is on {highest_category}.")
            
    else:
        insights.append("No transactions added yet. Start by adding your income and expenses.")

    return render_template(
        'dashboard/index.html', 
        total_income=total_income,
        total_expense=total_expense,
        current_balance=current_balance,
        recent_transactions=recent_transactions,
        highest_category=highest_category,
        insights=insights,
        chart_json_1=chart_json_1,
        chart_json_2=chart_json_2
    )
