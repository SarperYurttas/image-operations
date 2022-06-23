import os

import requests
from flask import redirect, render_template, request, url_for
from PIL import Image

from image_operations import app

from .operations import remove_background, resize_img

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class Context(object):  # Singleton class
    _instance = None
    data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Context, cls).__new__(cls)
        return cls._instance

    def error(self, msg='Unknown error!', logo=True):
        self.data['error'] = msg
        if logo:
            self.data['img_name'] = 'io_logo.png'

    def reset(self):
        self.data = {
            'error': None,
            'img_name': 'io_logo.png',
            'img_path': os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.png'),
        }


context = Context()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/result', methods=['GET', 'POST'])
def result():
    if context.data is None:
        return redirect('/')

    return render_template('result.html', context=context.data)


@app.route('/resize', methods=['GET', 'POST'])
def resize():
    if context.data is None:
        return redirect('/')
    if request.method == 'POST':
        if request.form.get('textbox') == ' ':
            context.error(msg='Enter resize factor', logo=False)
            return render_template('resize.html', context=context.data)

        elif request.form.get('textbox').strip().isnumeric():
            factor = int(request.form.get('textbox'))
            context.data['error'] = None
            if factor > 4:
                context.error(msg='Factor is too high', logo=False)
                return render_template('resize.html', context=context.data)

            resize_img(context.data['img_path'], factor=factor, method='bilinear')
            context.data['img_name'] = 'cached_img_resized.png'
            return redirect('/result')

        else:
            context.error(msg='Factor must be numeric', logo=False)
            return render_template('resize.html', context=context.data)

    return render_template('resize.html', context=context.data)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if context.data is None:
        return redirect('/')
    if request.method == 'POST':
        if request.form.get('button1') == 'Remove Background':

            remove_background(context.data['img_path'])
            context.data['img_name'] = 'cached_img_bgremoved.png'
            return redirect('/result')

        elif request.form.get('button2') == 'Resize':
            return redirect('/resize')

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.png'))
            context.data['img_name'] = 'cached_img.png'
            return redirect('/menu')

    return render_template('index.html', context=context.data)
