from flask import Flask, render_template, flash
from core.route import blueprints
import os
from flask_cors import CORS
import logging.handlers
from core.database import db
from flask_migrate import Migrate
from core import utils, constants
import settings


# Create APP
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors_config = {
  "origins": ["http://assets.crossref.org"]
}
CORS(app, resources={r"/*": cors_config})

utils.set_base_path(app.root_path)
app.config.from_object(settings)
utils.set_app_config(app.config)

blueprints.register_blueprints(app)

db.init_app(app)
migrate = Migrate(app, db)


# Logger configuration
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger(__name__)

fileHandler = logging.handlers.RotatingFileHandler(os.path.join(app.root_path, "logs", "app.log"),
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
    signed_in, info, session_expired = utils.signed_in_info()
    context_dict = {'signed_in': signed_in, 'orcid_info':info}
    if session_expired:
        flash(constants.ORCID_SESSION_EXPIRED, constants.MESSAGE_TYPE_WARN)
    return context_dict


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000), debug=os.environ.get("DEBUG", False))
