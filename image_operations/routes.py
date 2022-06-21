import os

import requests
from flask import flash, redirect, render_template, request
from PIL import Image

from image_operations import app

from .operations import resize_img

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/resize', methods=['GET', 'POST'])
def resize():
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.jpg'))
            return render_template('index.html', filename='cached_img.jpg')

    return render_template('index.html', filename='logo_nb.png')
