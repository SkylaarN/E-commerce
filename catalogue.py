from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db
bp = Blueprint('catalogue', __name__)

@bp.route("/", methods=("GET", "POST"))
def catalogue():
    db = get_db()
    products = db.execute(
        "SELECT id ,cartegory, product_name, price, description"
        " FROM catalogue"
    ).fetchall()
    return render_template('catalogue/catalogue.html', products=products)



# @bp.route("/add_item", methods=("GET", "POST"))
def add_item_to_basket():
    pass

def remove_item_from_basket():
    pass