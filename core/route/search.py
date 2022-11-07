from flask import render_template
from flask import Blueprint
from flask import request
import core.constants as constants
import core.service.search_service as service


search = Blueprint('search', __name__)

home = Blueprint('', __name__)


@search.route('/works')
def works():
    if request.args and request.args['q']:
        items, page = service.search_query(constants.CATEGORY_WORKS, request)
        page['name'] = constants.CATEGORY_WORKS
        return render_template("results.html", items=items, page=page)

    return render_template("splash.html")


@home.route('/')
def index():
    page = {'name': constants.CATEGORY_WORKS}
    return render_template("splash.html", page=page)