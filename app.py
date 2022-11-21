from flask import Flask, render_template
from core.route.search import search, home, help
import os
import logging
import logging.handlers

# Create APP
app = Flask(__name__)
app.secret_key = os.urandom(16)


# Logger configuration
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger(__name__)

fileHandler = logging.handlers.RotatingFileHandler(os.path.join(app.root_path,"app.log"),
                                                   maxBytes=(1048576*5), backupCount=5)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.INFO)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('requests').setLevel(logging.ERROR)


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


app.run(host='0.0.0.0', port=5000)
