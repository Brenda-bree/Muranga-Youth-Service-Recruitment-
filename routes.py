from flask import app, request, render_template, jsonify
from models import get_db_connection

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html', result=None)
    
@app.route('/verify', methods=['POST'])
def verify():
    id_number = request.form.get('id_number', '').strip()
    
    # Validation 1: Empty input
    if not id_number:
        return render_template('index.html', result={
            'status': 'ERROR',
            'message': 'Please enter an ID number.'
        })
    
    # Validation 2: Must contain only digits
    if not id_number.isdigit():
        return render_template('index.html', result={
            'status': 'ERROR',
            'message': 'ID number must contain only digits (0-9).'
        })
    
    # Validation 3: Must be exactly 8 digits
    if len(id_number) != 8:
        return render_template('index.html', result={
            'status': 'ERROR',
            'message': 'ID number must be exactly 9 digits.'
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
    
@app.route('/debug/ids')
def debug_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_number, name, cohort_number FROM recruitees LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])