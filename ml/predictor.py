import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
from utils.data_processing import get_transactions_df

def predict_next_month_expense(user_id):
    """
    Uses Scikit-learn Linear Regression to predict next month's total expenses
    based on historical monthly spending.
    """
    df = get_transactions_df(user_id)
    if df.empty:
        return None, "Not enough data for prediction."
        
    expenses_df = df[df['type'] == 'expense'].copy()
    if expenses_df.empty or len(expenses_df['date'].dt.to_period('M').unique()) < 3:
        return None, "Need at least 3 months of expense data to make a prediction."
        
    # Aggregate expenses by month
    expenses_df['month_index'] = (expenses_df['date'].dt.year - expenses_df['date'].dt.year.min()) * 12 + expenses_df['date'].dt.month
    monthly_expenses = expenses_df.groupby('month_index')['amount'].sum().reset_index()
    
    if len(monthly_expenses) < 3:
        return None, "Need at least 3 months of expense data to make a prediction."

    # Prepare features (X) and target (y)
    X = monthly_expenses[['month_index']]
    y = monthly_expenses['amount']
    
    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next month
    last_month_index = monthly_expenses['month_index'].max()
    next_month_index = last_month_index + 1
    
    predicted_amount = model.predict(np.array([[next_month_index]]))[0]
    
    # Ensure prediction is non-negative
    predicted_amount = max(0, predicted_amount)
    
    return predicted_amount, "Success"
