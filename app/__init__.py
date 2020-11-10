from flask import Flask
from config import Config
from os.path import join, dirname, realpath


app = Flask(__name__,  static_url_path='/static')
app.config.from_object(Config)
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.html']
app.config['UPLOAD_PATH'] = join(dirname(realpath(__file__)), 'static/uploads/')


from app import routes

