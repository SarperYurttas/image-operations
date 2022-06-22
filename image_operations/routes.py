import os

import requests
from flask import render_template, request, redirect
from PIL import Image

from image_operations import app

from .operations import resize_img, remove_bg

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/resize', methods=['GET', 'POST'])
def resize():
    """Deprecated
    """
    url = request.args.get('img_url', default=0)
    factor = int(request.args.get('factor', default=2))
    method = request.args.get('method', default='bilinear')

    if url == 0:
        return 'failed'

    response = requests.get(url=url, stream=True)
    if response.status_code > 200:
        return f'failed, status_code = {response.status_code}'

    img = Image.open(response.raw)
    resized_img = resize_img(img=img, factor=factor, method=method)
    resized_img.save('image_operations/static/cached_img.jpg')

    return render_template('resize.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


context = {
    'error': None,
    'img_name': 'logo_nb.png',
    'op_mode': False
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if context['op_mode']:
            context['error'] = None
            if request.form.get('button1') == 'Remove Background':
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.jpg')
                remove_bg(image_path)
                context['img_name'] = 'cached_img_bgremoved.png'
                return render_template('index.html', context=context)
            
            elif request.form.get('button2') == 'Resize':
                # TO DO
                app.logger.info('second_button pressed')
        else:                
            if 'file' not in request.files:
                context['error'] = 'Choose file first'
                return render_template('index.html', context=context)

            file = request.files['file']
            if file.filename == '':
                context['error'] = 'Choose file first'
                return render_template('index.html', context=context)

            if file and allowed_file(file.filename):
                context['error'] = None
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.jpg'))
                context['img_name'] = 'cached_img.jpg'
                context['op_mode'] = True
                return render_template('index.html', context=context)

            
    return render_template('index.html', context=context)
