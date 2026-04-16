from flask import Flask

def create_app():
    """Create and configure the Flask applicatio"""
    app = Flask(__name__)
    return app

def run():
    try:
        app = create_app()
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting the application: {e}")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"Unhandled exception: {e}")