from flask import Flask
import logging


app = Flask(__name__)
app.config["DEBUG"] = True
logging.basicConfig(level=logging.DEBUG)

from app import routes
