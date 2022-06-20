from flask import Flask

app = Flask(__name__)

from image_operations import routes

app.run(host='0.0.0.0', port=8080, debug=True)
