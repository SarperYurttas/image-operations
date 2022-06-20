from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = 'image_operations/static/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from image_operations import routes

app.run(host='0.0.0.0', port=8080, debug=True)
