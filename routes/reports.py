import os
import csv
from flask import Blueprint, render_template, send_file, flash, request, redirect, url_for
from flask_login import login_required, current_user
from models import Transaction
from extensions import db
from sqlalchemy import func
from utils.pdf_generator import generate_financial_report
from datetime import datetime

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
@login_required
def index():
    return render_template('reports/index.html')

@reports_bp.route('/reports/download_pdf')
@login_required
def download_pdf():
    # Calculate totals
    total_income = db.session.query(func.sum(Transaction.amount)).filter_by(
        user_id=current_user.id, type='income'
    ).scalar() or 0.0
    
    total_expense = db.session.query(func.sum(Transaction.amount)).filter_by(
        user_id=current_user.id, type='expense'
    ).scalar() or 0.0
    
    totals = {
        'income': total_income,
        'expense': total_expense,
        'balance': total_income - total_expense
    }
    
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    # Path for temporary PDF
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
    filename = f"report_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(reports_dir, filename)
    
    # Generate PDF
    generate_financial_report(current_user, transactions, totals, file_path)
    
    return send_file(file_path, as_attachment=True, download_name="Financial_Report.pdf")

@reports_bp.route('/reports/export_csv')
@login_required
def export_csv():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
    filename = f"transactions_{current_user.id}.csv"
    file_path = os.path.join(reports_dir, filename)
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Category', 'Type', 'Amount', 'Payment Method', 'Description'])
        for tx in transactions:
            writer.writerow([
                tx.date.strftime('%Y-%m-%d'),
                tx.category.name,
                tx.type,
                tx.amount,
                tx.payment_method,
                tx.description
            ])
            
    return send_file(file_path, as_attachment=True, download_name="Transactions_Export.csv")
