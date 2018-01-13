import os
import logging
from flask import Flask
from app.upload_book.controllers import uploader


LOG_DIR = os.getenv("LOG_DIR", "./")

logging.basicConfig(
    format="[%(asctime)s] [%(threadName)s] [%(levelname)s] [%(name)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "upload.log")),
        logging.StreamHandler()
    ],
    level=logging.INFO)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.register_blueprint(uploader, url_prefix='/')


@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File app Too Large', 413
