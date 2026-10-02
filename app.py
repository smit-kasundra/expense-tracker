from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager
from models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transactions import transactions_bp
    from routes.budgets import budgets_bp
    from routes.goals import goals_bp
    from routes.analytics import analytics_bp
    from routes.reports import reports_bp

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='')
    app.register_blueprint(transactions_bp, url_prefix='')
    app.register_blueprint(budgets_bp, url_prefix='')
    app.register_blueprint(goals_bp, url_prefix='')
    app.register_blueprint(analytics_bp, url_prefix='')
    app.register_blueprint(reports_bp, url_prefix='')


    # Add a basic index route redirecting to login or dashboard
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
