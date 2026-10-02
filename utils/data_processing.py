import pandas as pd
from models import Transaction, Category

def get_transactions_df(user_id):
    # Fetch transactions and related category names
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    if not transactions:
        return pd.DataFrame()

    data = []
    for tx in transactions:
        data.append({
            'id': tx.id,
            'date': tx.date,
            'amount': tx.amount,
            'type': tx.type,
            'category': tx.category.name,
            'payment_method': tx.payment_method
        })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df
