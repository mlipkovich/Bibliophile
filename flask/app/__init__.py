from flask import Flask
from flask.app import uploader

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

app.register_blueprint(uploader, url_prefix='/')


@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File app Too Large', 413
