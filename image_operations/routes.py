import os

import requests
from flask import render_template, request, redirect
from PIL import Image

from image_operations import app

from .operations import resize_img, remove_bg

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CONTEXT = {
    'error': None,
    'img_name': 'logo_nb.png',
    'isFile': False
}


class Context(object): # Singleton class
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Context, cls).__new__(cls)
        return cls._instance
    
    def error(self, msg='Unknown error!'):
        self.data['error'] = msg
        self.data['img_name'] = 'logo_nb.png'
    
    def reset(self):
        self.data = {
        'error': None,
        'img_name': 'logo_nb.png',
        'isFile': False
        }
    
context = Context()
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    app.logger.info(CONTEXT)
    if request.method == 'POST':
        if request.form.get('button1') == 'Remove Background':
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.jpg')
            remove_bg(image_path)
            CONTEXT['img_name'] = 'cached_img_bgremoved.png'
            return render_template('menu.html', context=context.data)

        elif request.form.get('button2') == 'Resize':
            # TO DO
            app.logger.info('second_button pressed')
            
    return render_template('menu.html', context=context.data)


@app.route('/', methods=['GET', 'POST'])
def index():
    context.reset()
    if request.method == 'POST':
        if 'file' not in request.files:
            context.error('Choose file first!')
            return render_template('index.html', context=context.data)

        file = request.files['file']
        if file.filename == '':
            context.error('Choose file first!')
            return render_template('index.html', context=context.data)

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.jpg'))
            context.data['img_name'] = 'cached_img.jpg'
            context.data['isFile'] = True
            return redirect('/menu')

    return render_template('index.html', context=context.data)
