from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required, admin_login_required
from .db import get_db
bp = Blueprint('catalogue', __name__, url_prefix='/product')

@bp.route("/", methods=("GET", "POST"))
def catalogue():
    db = get_db()
    products = db.execute(
        "SELECT id ,cartegory, product_name, price, description"
        " FROM catalogue"
    ).fetchall()
    return render_template('catalogue/catalogue.html', products=products)

@bp.route('/create', methods=('GET', 'POST'))
@admin_login_required
def create():
    if request.method == 'POST':
        cartegory = request.form['cartegory']
        product_name = request.form['product_name']
        price = request.form['price']
        description= request.form['description']
        error = None
        if not product_name:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO catalogue (cartegory, product_name, price, description)'
                ' VALUES (?, ?, ?, ?)',
            (cartegory, product_name, price, description)
            )
            db.commit()
            return redirect(url_for('catalogue.catalogue'))
    return render_template('catalogue/create.html')



# @bp.route("/add_item", methods=("GET", "POST"))
def add_item_to_basket():
    pass

def remove_item_from_basket():
    pass