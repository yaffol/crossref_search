import requests
import core.constants as constants
import calendar
import furl
from flask_paginate import Pagination, get_page_parameter

import core.test_data
import core.utils as utils


def sort_type(request):
    sort_by = 'relevance'
    if 'sort' in request.args:
        sort_by = request.args['sort']

    return sort_by


def get_api_url(category, request):
    """
    Return the Crossref API url depending on the category
    :param category: API category
    :param query: api query parameter
    :return:
    """

    query = request.args['q']

    url = None
    if category == constants.CATEGORY_WORKS:
        url = constants.WORKS_API_URL + "?query=" + query

    if 'page' in request.args:
        page_value = int(request.args['page'])
        offset = (page_value - 1) * constants.ROWS_PER_PAGE
        url += '&offset=' + str(offset)

    if 'publisher' in request.args:
        url += '&query.container-title=' + request.args['publisher']

    sort_by = sort_type(request)
    if sort_by == 'year':
        sort_by = 'published'
    url += '&sort=' + sort_by
    url += '&rows=' + str(constants.ROWS_PER_PAGE)

    return url


def get_request_url(request, exclude):
    """
    Return the request url removing the exclude parameters from query string
    :param request: request object
    :param exclude: array of exclude parameters
    :return:
    """
    f = furl.furl(request.url)
    if isinstance(exclude, list):
        f.remove(exclude)
    elif isinstance(exclude, str):
        f.remove(exclude.split(','))
    return f.url


def get_pagination_url(request):
    url = get_request_url(request, ['page'])
    url += '&page={0}'
    return url


def format_item_type(item):
    item_type = None
    if "type" in item:
        item_type = item["type"]
        item_type = item_type.replace('-', ' ').upper()
    return item_type


def format_published_date(item):
    published_date = None
    published = None
    if "published-print" in item:
        published = item["published-print"]
    elif "published-online" in item:
        published = item["published-online"]

    if published:
        if "date-parts" in published:
            date_parts = published["date-parts"][0]
            date_parts_len = len(date_parts)
            published_date = ""
            if date_parts_len > 2:
                published_date = str(date_parts[2]) + " "
            if date_parts_len > 1:
                published_date += calendar.month_name[date_parts[1]] + " "
            if date_parts_len > 0:
                published_date += str(date_parts[0])

    return published_date


def get_container_title(item):
    container_title = None

    if "container-title" in item and len(item["container-title"]) > 0:
        container_title = item["container-title"][0]

    return container_title


def get_alternative_id(item):
    if 'alternative-id' in item:
        return item['alternative-id']
    else:
        return None


def get_items(obj):
    items = []
    total = 0
    if obj["message"]["total-results"]:
        total = obj["message"]["total-results"]
    if obj["message"]["items"]:
        for item in obj["message"]["items"]:
            items.append({
                "title": item["title"][0] if 'title' in item else '',
                "type": format_item_type(item),
                "published_date": format_published_date(item),
                "publication": get_container_title(item),
                "display_doi": utils.get_doi_url(item['DOI']),
                "doi": item['DOI'],
                "supplementary_ids": get_alternative_id(item)
            })

    return items, total


def search_query(category, request):
    url = get_api_url(category, request)
    res = requests.get(url)

    if res.status_code == 200:
        items, total = get_items(core.test_data.test_result)
        # items, total = get_items(res.json())
        page_number = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page_number, total=total, search=False, per_page=constants.ROWS_PER_PAGE,
                                href=get_pagination_url(request))
        page = {'pagination': pagination,
                'sort_url': get_request_url(request, ['sort']),
                'publisher_url': get_request_url(request, ['publisher']),
                'sort_type': sort_type(request),
                'api_url': constants.WORKS_API_URL
                }
        return items, page
