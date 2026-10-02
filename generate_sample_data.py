import random
from datetime import datetime, timedelta
from app import create_app
from extensions import db
from models import User, Category, Transaction, Budget, FinancialGoal
from werkzeug.security import generate_password_hash

def populate_db():
    app = create_app()
    with app.app_context():
        # Clear existing data for demo purposes (optional, be careful)
        # db.drop_all()
        # db.create_all()

        # Check if demo user exists
        demo_user = User.query.filter_by(email='demo@student.com').first()
        if not demo_user:
            demo_user = User(
                username='demo_student',
                email='demo@student.com',
                password_hash=generate_password_hash('password123')
            )
            db.session.add(demo_user)
            db.session.commit()
            
            # Categories
            default_categories = [
                ('Food', 'expense'), ('Travel', 'expense'), ('Shopping', 'expense'),
                ('Education', 'expense'), ('Bills', 'expense'), ('Healthcare', 'expense'),
                ('Entertainment', 'expense'), ('Rent', 'expense'), ('Transportation', 'expense'),
                ('Salary', 'income'), ('Freelance', 'income'), ('Scholarship', 'income'), ('Investment', 'income')
            ]
            
            cats = {}
            for name, ctype in default_categories:
                cat = Category(name=name, type=ctype, is_default=True, user_id=demo_user.id)
                db.session.add(cat)
                db.session.commit()
                cats[name] = cat
                
            # Add sample transactions for the past 4 months
            payment_methods = ['Cash', 'UPI', 'Debit Card', 'Credit Card']
            
            for i in range(120): # 120 days ago to now
                tx_date = datetime.utcnow().date() - timedelta(days=i)
                
                # Income (e.g., Salary on 1st of month)
                if tx_date.day == 1:
                    t = Transaction(amount=50000.0, type='income', date=tx_date, description="Monthly Salary",
                                    payment_method="Net Banking", category_id=cats['Salary'].id, user_id=demo_user.id)
                    db.session.add(t)
                
                # Random expenses
                if random.random() > 0.3: # 70% chance of expense on a day
                    expense_cat = random.choice(['Food', 'Travel', 'Shopping', 'Entertainment', 'Bills'])
                    amount = round(random.uniform(100, 2500), 2)
                    t = Transaction(amount=amount, type='expense', date=tx_date, description=f"Bought {expense_cat}",
                                    payment_method=random.choice(payment_methods), category_id=cats[expense_cat].id, user_id=demo_user.id)
                    db.session.add(t)
                    
            # Add some budgets for current month
            current_month = datetime.utcnow().month
            current_year = datetime.utcnow().year
            
            db.session.add(Budget(amount=10000, month=current_month, year=current_year, category_id=cats['Food'].id, user_id=demo_user.id))
            db.session.add(Budget(amount=5000, month=current_month, year=current_year, category_id=cats['Entertainment'].id, user_id=demo_user.id))
            
            # Add a goal
            db.session.add(FinancialGoal(name="New Laptop", target_amount=70000, current_amount=35000, 
                                         deadline=datetime.utcnow().date() + timedelta(days=180), user_id=demo_user.id))
            
            db.session.commit()
            print("Successfully populated database with demo user 'demo@student.com' (password: password123).")
        else:
            print("Demo user already exists.")

if __name__ == '__main__':
    populate_db()
