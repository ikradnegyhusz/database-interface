from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Egyen
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        jelszo = request.form.get('password')

        egyen = Egyen.query.filter_by(email=email).first()
        if egyen:
            if check_password_hash(egyen.jelszo, jelszo):
                flash('Sikeres bejelentkezés!', category='success')
                login_user(egyen, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('A jelszó nem helyes.', category='error')
        else:
            flash('Ez az email nincs regisztrálva.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))