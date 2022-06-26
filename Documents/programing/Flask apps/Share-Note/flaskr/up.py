from distutils.log import error
from turtle import title
from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from .models import Note
from . import db
import os 
from os import path
import datetime

up = Blueprint('up', __name__)

@up.route('/up', methods=['GET'])
@login_required
def up_get():
    if request.method == 'GET':
        return render_template('up.html', user=current_user)
@up.route('/up', methods=['POST'])
@login_required
def up_post():
    if request.method == 'POST':
        f = request.files.get('image')

        data = request.form.get('data')
        title = request.form.get('title')
    

        filename = secure_filename(f.filename)
        UPLOAD_FOLDER = 'flaskr/static/image'
        filepath = UPLOAD_FOLDER + filename
        if len(title)<1:
            flash('名前を入力してください')
        elif len(data)<1:
            flash('ノートを入力してください')
        elif len(filename)<1: 
            flash('ファイルをアップロードしてください')
        else:
            f.save(filepath)
            
            NOW = datetime.datetime.now()
            
            new_filename = os.path.join(f.filename.rsplit('.',1)[0] + '_' + NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + f.filename.rsplit('.',1)[1])
            
            new_filepath = os.path.join(UPLOAD_FOLDER, new_filename)
            os.rename(filepath, new_filepath)

            new_note = Note(data=data, title=title, filename=new_filename, user_id=current_user.id, author=current_user.name)
            db.session.add(new_note)
            db.session.commit()
            flash('note added')
    return render_template('up.html', user=current_user, data=data, title=title)