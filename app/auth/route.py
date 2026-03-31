from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User
from app.forms import LoginForm
from app.auth import bp

@bp.route('/register')
def redirect_register():
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard') if current_user.is_admin else url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    return render_template('auth/login.html', form=form)

from flask_login import logout_user, login_required

# ... (ton code existant pour login) ...

@bp.route('/logout')
@login_required
def logout():
    logout_user() # Cette fonction de Flask-Login déconnecte l'utilisateur
    flash('Vous avez été déconnecté avec succès.', 'info')
    return redirect(url_for('main.index')) # Redirige vers la page d'accueil de ton portfolio