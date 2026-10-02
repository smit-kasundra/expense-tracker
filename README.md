# Personal Finance & Expense Analyzer

A complete, professional Python web application built with Flask for a 5th-semester college project. It helps users manage their income, expenses, budgets, financial goals, and generates insightful analytics and PDF reports.

## Features
- **User Authentication:** Secure login and registration with hashed passwords.
- **Transaction Management:** Add, edit, delete, and view income/expenses.
- **Budgeting:** Set monthly category budgets and track spending limits.
- **Financial Goals:** Define savings targets and track progress.
- **Dashboard & Analytics:** Interactive Plotly charts and Pandas data aggregation.
- **Expense Prediction:** Machine learning (Scikit-Learn) to forecast future expenses based on historical data.
- **Reporting:** Download PDF reports and export transaction data to CSV.

## Technologies Used
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Database:** SQLite
- **Analytics & ML:** Pandas, NumPy, Scikit-Learn
- **Visualization:** Plotly
- **Reporting:** ReportLab

## Setup Instructions

1. **Install Dependencies:**
   Make sure you have Python 3.x installed. Run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Sample Data (Optional but Recommended for Demo):**
   Run the following script to create a demo user and populate the database with sample transactions, budgets, and goals:
   ```bash
   python generate_sample_data.py
   ```
   *Demo Login Credentials:*
   - Email: `demo@student.com`
   - Password: `password123`

3. **Run the Application:**
   ```bash
   python app.py
   ```
   The app will run at `http://127.0.0.1:5000/`.

4. **Run Tests:**
   ```bash
   pytest
   ```
