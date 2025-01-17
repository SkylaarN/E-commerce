import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

#register blueprint
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'

        elif not password:
            error = 'Password is required.'

        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
            ).fetchone() is not None: error = 'User {} is already registered.'.format(username)
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for('auth.login'))
            
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
    
        if user is None:
            error = 'Incorrect username.'

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
#####
        if error  is not None: 
            flash(error)
            return redirect(url_for('auth.login'))
        
        return redirect(url_for('blog.index'))

    return render_template('auth/login.html')


#############
#  Admin auth


#register blueprint
@bp.route('/admin_register', methods=('GET', 'POST'))
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'

        elif not password:
            error = 'Password is required.'

        elif db.execute(
            'SELECT id FROM amdin WHERE username = ?', (username,)
            ).fetchone() is not None: error = 'User {} is already registered.'.format(username)
        
        if error is None:
            db.execute(
                'INSERT INTO amdin (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for('auth.admin_login'))
            
        flash(error)

    return render_template('auth/admin_register.html')

@bp.route('/admin', methods=('GET', 'POST'))
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        user = db.execute(
            'SELECT * FROM amdin WHERE username = ?', (username,)
        ).fetchone()
    
        if user is None:
            error = 'Username does not exist.'

        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

        if error  is not None: 
            flash(error)
            return redirect(url_for('auth.admin_login'))
        
        return redirect(url_for('admin.create'))

    return render_template('auth/admin_login.html')

#############

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.admin_register'))
        return view(**kwargs)
    return wrapped_view