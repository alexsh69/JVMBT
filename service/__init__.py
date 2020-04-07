from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging


logger = logging.getLogger(__name__)

app = Flask(__name__)
logger.info("App initialized!")
CORS(app=app, resources="*", headers='Content-type')
api = Api(app=app)
logger.info("Api initialized!")


import service.views
