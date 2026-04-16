from flask import request, render_template
from models import get_db_connection

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html', result=None)
    
    @app.route('/verify', methods=['POST'])
    def verify():
        id_number = request.form.get('id_number', '').strip()
        
        if not id_number:
            return render_template('index.html', result={
                'status': 'ERROR',
                'message': 'Please enter an ID number.'
            })
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, cohort_number FROM recruitees WHERE id_number = ?",
            (id_number,)
        )
        existing = cursor.fetchone()
        conn.close()
        
        if existing:
            return render_template('index.html', result={
                'status': 'REJECTED',
                'message': f"{existing['name']} is already in Cohort {existing['cohort_number']}."
            })
        else:
            return render_template('index.html', result={
                'status': 'APPROVED',
                'message': "Clear for registration in Cohort 9."
            })