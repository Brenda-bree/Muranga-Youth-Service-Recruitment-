from flask import Flask
from models import init_database
from routes import register_routes
from flask_login import LoginManager
from models import init_database


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from models import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return type('User', (), {
            'is_authenticated': True,
            'is_active': True,
            'is_anonymous': False,
            'get_id': lambda: str(user['id']),
            'role': user['role']
        })()
    return None

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'incorrect.997@BreastFriend'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    init_database()
    
    # Register routes
    register_routes(app)
    
    return app

def run():
    try:
        app = create_app()
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"Error starting the application: {e}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"Unhandled exception: {e}")