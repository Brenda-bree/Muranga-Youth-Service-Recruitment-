from flask import Flask

def create_app():
    """Create and configure the Flask applicatio"""
    app = Flask(__name__)
    return app