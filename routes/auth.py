from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Category
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
            
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Add default categories for the new user
        default_categories = [
            ('Food', 'expense'), ('Travel', 'expense'), ('Shopping', 'expense'),
            ('Education', 'expense'), ('Bills', 'expense'), ('Healthcare', 'expense'),
            ('Entertainment', 'expense'), ('Rent', 'expense'), ('Transportation', 'expense'),
            ('Salary', 'income'), ('Freelance', 'income'), ('Business', 'income'),
            ('Scholarship', 'income'), ('Investment', 'income'), ('Other', 'income'), ('Other', 'expense')
        ]
        
        for cat_name, cat_type in default_categories:
            cat = Category(name=cat_name, type=cat_type, is_default=True, user_id=new_user.id)
            db.session.add(cat)
            
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
