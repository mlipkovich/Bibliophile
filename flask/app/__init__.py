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
app.register_blueprint(uploader, url_prefix='/')

