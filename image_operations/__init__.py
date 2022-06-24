from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = 'image_operations/static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
