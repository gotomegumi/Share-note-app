from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import Note
from . import db
import os 
from os import path
import datetime

update = Blueprint('update', __name__)

# @update.route('/update', methods=['GET'])
# def update_get(id):
#     if request.method == 'GET':
#         note = Note.query.filter_by(id=id).first()
#         return render_template('update.html', note=note, user=current_user)

@update.route('/update', methods=['POST'])
def update_post():
    if request.method == 'POST':
        id = request.form.get('id')
        data = request.form.get('data')
        title = request.form.get('title')
        note = Note.query.filter_by(id=id).first()

        if current_user.id == note.user_id:


            note.data = data
            note.title = title
            db.session.commit()
    return redirect('/')

