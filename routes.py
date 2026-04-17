from flask import request, render_template, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt
from models import get_user_by_username, get_db_connection
from auth import staff_required, admin_required, User

def register_routes(app):
    
    @app.route('/')
    @staff_required
    def index():
        return render_template('index.html', result=None)
    
    @app.route('/verify', methods=['POST'])
    @staff_required
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
            name_term = request.form.get('id_number', '').strip()
            
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
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            if not username or not password:
                flash('Please enter username and password.', 'error')
                return render_template('login.html')
            
            user = get_user_by_username(username)
            if user and bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):
                user_obj = User(user['id'], user['username'], user['role'])
                login_user(user_obj)
                flash(f'Welcome back, {username}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))
    
    @app.route('/debug/ids')
    @admin_required
    def debug_ids():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_number, name, cohort_number FROM recruitees LIMIT 10")
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])
    
    @app.route('/search/names', methods=['GET'])
    @staff_required
    def search_names():
        query = request.args.get('q', '').strip()
        if len(query) < 2:
            return jsonify([])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_number, name, gender, size, phone_number, cohort_number FROM recruitees WHERE LOWER(name) LIKE ? LIMIT 10",
            (f'%{query.lower()}%',)
        )
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])


    @app.route('/admin/staff')
    @admin_required
    def admin_staff():
        from models import get_all_users
        users = get_all_users()
        return render_template('admin_staff.html', users=users, current_user=current_user)
    
    @app.route('/admin/staff/add', methods=['POST'])
    @admin_required
    def admin_add_user():
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'staff')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('admin_staff'))
        
        if len(password) < 4:
            flash('Password must be at least 4 characters.', 'error')
            return redirect(url_for('admin_staff'))
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        from models import create_user
        success = create_user(username, hashed.decode('utf-8'), role)
        
        if success:
            flash(f'User "{username}" created successfully as {role}.', 'success')
        else:
            flash(f'Username "{username}" already exists.', 'error')
        
        return redirect(url_for('admin_staff'))
    
    @app.route('/admin/staff/delete/<int:user_id>')
    @admin_required
    def admin_delete_user(user_id):
        # onvert to int and compare
        current_user_id = int(current_user.id)
        target_user_id = int(user_id)
        
        # Prevent admin from deleting themselves
        if target_user_id == current_user_id:
            flash('❌ You cannot delete your own account. This action has been blocked.', 'error')
            return redirect(url_for('admin_staff'))
        
        from models import delete_user_by_id
        if delete_user_by_id(target_user_id):
            flash(f'✅ User deleted successfully.', 'success')
        else:
            flash(f'❌ User not found or could not be deleted.', 'error')
        
        return redirect(url_for('admin_staff'))

    @app.route('/admin/database')
    @admin_required
    def admin_database():
        from models import get_all_recruitees
        recruitees = get_all_recruitees()
        return render_template('admin_database.html', recruitees=recruitees)

    @app.route('/admin/database/add', methods=['GET', 'POST'])
    @admin_required
    def admin_add_recruitee():
        if request.method == 'POST':
            id_number = request.form.get('id_number', '').strip()
            name = request.form.get('name', '').strip()
            gender = request.form.get('gender', '')
            size = request.form.get('size', '')
            phone = request.form.get('phone', '').strip()
            cohort = request.form.get('cohort', '').strip()
            
            # Basic validation
            if not id_number or not name or not cohort:
                flash('ID Number, Name, and Cohort are required.', 'error')
                return redirect(url_for('admin_add_recruitee'))
            if len(id_number) != 9 or not id_number.isdigit():
                flash('ID Number must be exactly 9 digits.', 'error')
                return redirect(url_for('admin_add_recruitee'))
            
            from models import add_recruitee
            success = add_recruitee(id_number, name, gender, size, phone, cohort)
            if success:
                flash(f'Recruitee {name} added successfully.', 'success')
                return redirect(url_for('admin_database'))
            else:
                flash(f'ID Number {id_number} already exists.', 'error')
                return redirect(url_for('admin_add_recruitee'))
        
        return render_template('admin_database_form.html', action='Add', recruitee=None)

    @app.route('/admin/database/edit/<id_number>', methods=['GET', 'POST'])
    @admin_required
    def admin_edit_recruitee(id_number):
        from models import get_recruitee_by_id, update_recruitee
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            gender = request.form.get('gender', '')
            size = request.form.get('size', '')
            phone = request.form.get('phone', '').strip()
            cohort = request.form.get('cohort', '').strip()
            
            if not name or not cohort:
                flash('Name and Cohort are required.', 'error')
                return redirect(url_for('admin_edit_recruitee', id_number=id_number))
            
            success = update_recruitee(id_number, name, gender, size, phone, cohort)
            if success:
                flash(f'Recruitee {name} updated successfully.', 'success')
                return redirect(url_for('admin_database'))
            else:
                flash('Update failed.', 'error')
                return redirect(url_for('admin_edit_recruitee', id_number=id_number))
        
        recruitee = get_recruitee_by_id(id_number)
        if not recruitee:
            flash('Recruitee not found.', 'error')
            return redirect(url_for('admin_database'))
        return render_template('admin_database_form.html', action='Edit', recruitee=recruitee)

    @app.route('/admin/database/delete/<id_number>')
    @admin_required
    def admin_delete_recruitee(id_number):
        from models import delete_recruitee
        if delete_recruitee(id_number):
            flash('Recruitee deleted successfully.', 'success')
        else:
            flash('Recruitee not found.', 'error')
        return redirect(url_for('admin_database'))

    @app.route('/profile')
    @login_required
    def profile():
        from models import get_user_by_id
        user = get_user_by_id(current_user.id)
        return render_template('profile.html', user=user)

    def get_user_by_id(user_id):
    """Fetch a user by ID (excludes password)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user