from django.shortcuts import redirect, render
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user

auth = Blueprint('auth', __name__, url_prefix='/')

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('ユーザーは既に存在します')
        elif len(password1)<=4:
            flash('パスワードは5文字以上でおねがいします')
        elif len(email)<=7:
            flash('emailが短すぎます')
        elif len(name) == 0:
            flash('名前を入力してください')
        elif password1 != password2:
            flash('パスワードが一致しません')
        else:        
            new_user = User(name=name, password=generate_password_hash(password1, method='sha256'), email=email)
            db.session.add(new_user)
            db.session.commit() 
            login_user(new_user, remember=True)           
            flash('登録されました')
            return redirect(url_for('view.home'))
    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('view.home'))

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('ログインしました')
                login_user(user, remember=True)
                return redirect(url_for('view.home'))
            else:
                flash('パスワードが違います')
        else:
            flash('このemailのユーザーが存在しません')
    return render_template('login.html', user=current_user)
