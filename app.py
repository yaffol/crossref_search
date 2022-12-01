from flask import Flask, render_template, session
from core.route.search import search, home, help
from core.route.orcid_auth import auth
import os
import logging
import logging.handlers
from core import utils, constants
import settings

# Create APP
app = Flask(__name__)

utils.set_base_path(app.root_path)
app.config.from_object(settings)
utils.set_app_config(app.config)


# Logger configuration
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger(__name__)

fileHandler = logging.handlers.RotatingFileHandler(os.path.join(app.root_path, "app.log"),
                                                   maxBytes=(1048576*5), backupCount=5)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.INFO)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('requests').setLevel(logging.ERROR)
formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(search, url_prefix='/search')
app.register_blueprint(help, url_prefix='/help')
app.register_blueprint(home, url_prefix='/')


@app.errorhandler(400)
def error_400(e):
    app.logger.error(e)
    return render_template('400.html'), 400


@app.errorhandler(401)
def error_401(e):
    app.logger.error(e)
    return render_template('401.html'), 401


@app.errorhandler(404)
def error_404(e):
    app.logger.error(e)
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500


@app.context_processor
def user_info():
    signed_in, info = utils.signed_in_info()
    context_dict = {'signed_in': signed_in, 'orcid_info':info}
    return context_dict


app.run(host='0.0.0.0', port=5050)
