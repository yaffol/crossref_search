from flask import Flask
from core.route.search import search, home, help


def create_app():
    app = Flask(__name__)

    app.register_blueprint(search, url_prefix='/search')
    app.register_blueprint(help, url_prefix='/help')
    app.register_blueprint(home, url_prefix='/')

    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
