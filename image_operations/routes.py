from PIL import Image
import requests
from flask import render_template, request, Flask
from .operations import resize_img

from image_operations import app


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
    resized_img.save('image_operations/static/img_cache.jpg')

    return render_template('resize.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
