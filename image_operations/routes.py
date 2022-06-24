import os
import secrets

from flask import redirect, render_template, request, session

from image_operations import app

from .operations import remove_background, resize_img

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.secret_key = 'gizli_sifre'


def raise_error(msg='Unknown error!', logo=True):
    session['context']['error'] = msg
    if logo:
        session['context']['img_name'] = 'io_logo.png'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/result', methods=['GET', 'POST'])
def result():
    if session['context']['img_name'] == 'io_logo.png':
        return redirect('/')

    return render_template('result.html', context=session['context'])


@app.route('/resize', methods=['GET', 'POST'])
def resize():
    if session['context']['img_name'] == 'io_logo.png':
        return redirect('/')

    if request.method == 'POST':
        if request.form.get('textbox') == ' ':
            raise_error(msg='Enter resize factor', logo=False)
            return render_template('resize.html', context=session['context'])

        elif request.form.get('textbox').strip().isnumeric():
            factor = int(request.form.get('textbox'))
            method = request.form.get('methods')
            session['context']['error'] = None

            if factor > 4:
                raise_error(msg='Factor is too high (max: 4)', logo=False)
                return render_template('resize.html', context=session['context'])

            resize_img(session['context']['img_path'], factor=factor, method=method)
            session['context']['img_name'] = 'cached_img_resized.png'
            return redirect('/result')

        else:
            raise_error(msg='Factor must be numeric', logo=False)
            return render_template('resize.html', context=session['context'])

    return render_template('resize.html', context=session['context'])


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if session['context']['img_name'] == 'io_logo.png':
        return redirect('/')

    if request.method == 'POST':
        if request.form.get('button1') == 'Remove Background':
            remove_background(session['context']['img_path'])
            session['context']['img_name'] = 'cached_img_bgremoved.png'
            return redirect('/result')

        elif request.form.get('button2') == 'Resize':
            return redirect('/resize')

    return render_template('menu.html', context=session['context'])


@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'error': None,
        'is_file_uploaded': False,
        'img_name': 'io_logo.png',
        'img_path': os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.png'),
    }
    session['context'] = context
    # app.logger.info(secrets.token_hex())
    if request.method == 'POST':
        if 'file' not in request.files:
            raise_error('Choose file first!')
            return render_template('index.html', context=session['context'])

        file = request.files['file']
        if file.filename == '':
            raise_error('Choose file first!')
            return render_template('index.html', context=session['context'])

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'cached_img.png'))
            session['context']['img_name'] = 'cached_img.png'
            session['context']['is_file_uploaded'] = 'cached_img.png'
            return redirect('/menu')

    return render_template('index.html', context=session['context'])
