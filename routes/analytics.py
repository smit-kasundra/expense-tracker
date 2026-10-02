from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ml.predictor import predict_next_month_expense
from utils.data_processing import get_transactions_df
import pandas as pd
import json
import plotly.express as px
import plotly.utils

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
def index():
    prediction, message = predict_next_month_expense(current_user.id)
    
    df = get_transactions_df(current_user.id)
    chart_json_trends = None
    
    if not df.empty:
        # Spending Trends Chart (Daily)
        expenses_df = df[df['type'] == 'expense']
        if not expenses_df.empty:
            daily_expenses = expenses_df.groupby('date')['amount'].sum().reset_index()
            fig = px.line(daily_expenses, x='date', y='amount', title='Daily Spending Trend')
            chart_json_trends = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template(
        'analytics/index.html',
        prediction=prediction,
        message=message,
        chart_json_trends=chart_json_trends
    )
