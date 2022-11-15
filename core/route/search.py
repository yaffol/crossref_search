from flask import render_template
from flask import Blueprint
from flask import request
import core.constants as constants
import core.service.search_service as service


search = Blueprint('search', __name__)

home = Blueprint('', __name__)

help = Blueprint('help', __name__)


@search.route('/works')
def works():
    if request.args and request.args['q']:
        items, page = service.search_query(constants.CATEGORY_WORKS, request)
        page['name'] = constants.CATEGORY_WORKS
        return render_template("results.html", items=items, page=page)

    page = {'name': constants.CATEGORY_WORKS}
    return render_template("splash.html", page=page)


@search.route('/funders/<id>')
def funder_search(id):
    if request.args and request.args['q']:
        items, page = service.search_query(constants.CATEGORY_FUNDERS, request)
        page['name'] = constants.CATEGORY_FUNDERS
        return render_template("results.html", items=items, page=page)

    page = {'name': constants.CATEGORY_FUNDERS}
    return render_template("funder_search.html", page=page)


@search.route('/funders')
def funders():
    if request.args and 'q' in request.args:
        items = service.search_query(constants.CATEGORY_FUNDERS, request)
        return items

    elif request.args and 'id' in request.args:
        items, page = service.search_query(constants.CATEGORY_FUNDERS, request)
        page['name'] = constants.CATEGORY_FUNDERS
        return render_template("results.html", items=items, page=page)

    page = {'name': constants.CATEGORY_FUNDERS}
    return render_template("funder_search.html", page=page)


@home.route('/')
def index():
    page = {'name': constants.CATEGORY_WORKS}
    return render_template("splash.html", page=page)


@help.route('/works')
def works_help():
    page = {'name': constants.CATEGORY_WORKS}
    return render_template("search_help.html", page=page)


