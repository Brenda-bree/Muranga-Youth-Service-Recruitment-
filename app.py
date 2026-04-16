from flask import Flask
from models import init_database
from routes import register_routes

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
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