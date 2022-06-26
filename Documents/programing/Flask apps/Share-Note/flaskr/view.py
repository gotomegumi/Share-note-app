# from crypt import methods
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from .models import Note
from . import db
import os

view = Blueprint('view', __name__, url_prefix='/')

@view.route('/', methods=['GET'])
def home():
    notes = Note.query.all()
    return render_template('home.html', notes=notes,user=current_user)

@view.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    note_delete = Note.query.filter_by(id=id).first()

    if current_user.id == note_delete.user_id:


        file = os.path.join('flaskr/static/image/', note_delete.filename)
        os.remove(file)

        db.session.delete(note_delete)
        db.session.commit()
    return redirect('/')

