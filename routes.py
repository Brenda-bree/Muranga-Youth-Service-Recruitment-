from flask import request, render_template, jsonify
from models import get_db_connection

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html', result=None)
    
    @app.route('/verify', methods=['POST'])
    def verify():
        search_type = request.form.get('search_type', 'id')
        
        if search_type == 'id':
            id_number = request.form.get('id_number', '').strip()
            
            if not id_number:
                return render_template('index.html', result={
                    'status': 'ERROR',
                    'message': 'Please enter an ID number.'
                })
            
            if not id_number.isdigit():
                return render_template('index.html', result={
                    'status': 'ERROR',
                    'message': 'ID number must contain only digits (0-9).'
                })
            
            if len(id_number) != 9:
                return render_template('index.html', result={
                    'status': 'ERROR',
                    'message': 'ID number must be exactly 9 digits.'
                })
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, gender, size, phone_number, cohort_number FROM recruitees WHERE id_number = ?",
                (id_number,)
            )
            existing = cursor.fetchone()
            conn.close()
            
        else:  
            name_term = request.form.get('id_number', '').strip()  # reusing same field name
            
            if not name_term:
                return render_template('index.html', result={
                    'status': 'ERROR',
                    'message': 'Please enter a name to search.'
                })
            
            if len(name_term) < 2:
                return render_template('index.html', result={
                    'status': 'ERROR',
                    'message': 'Please enter at least 2 characters for name search.'
                })
            
            conn = get_db_connection()
            cursor = conn.cursor()
            # Partial match, case-insensitive, return first match
            cursor.execute(
                "SELECT name, gender, size, phone_number, cohort_number FROM recruitees WHERE LOWER(name) LIKE ? LIMIT 1",
                (f'%{name_term.lower()}%',)
            )
            existing = cursor.fetchone()
            conn.close()
        
        if existing:
            return render_template('index.html', result={
                'status': 'REJECTED',
                'message': f"{existing['name']} is already in Cohort {existing['cohort_number']}.",
                'details': {
                    'name': existing['name'],
                    'gender': existing['gender'],
                    'size': existing['size'],
                    'phone': existing['phone_number'],
                    'cohort': existing['cohort_number']
                }
            })
        else:
            return render_template('index.html', result={
                'status': 'APPROVED',
                'message': "Clear for registration in Cohort 9."
            })
    
    @app.route('/debug/ids')
    def debug_ids():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_number, name, cohort_number FROM recruitees LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])