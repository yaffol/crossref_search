import requests
import core.constants as constants
import calendar
import furl
from flask_paginate import Pagination, get_page_parameter
from flask import escape

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

    url = None
    params = {}
    if category == constants.CATEGORY_WORKS:
        if 'q' in request.args:
            url = constants.WORKS_API_URL + "?query=" + request.args['q']

        sort_by = sort_type(request)
        if sort_by == 'year':
            sort_by = 'published'
        url += '&sort=' + sort_by

    elif category == constants.CATEGORY_FUNDERS:
        if 'q' in request.args:
            url = constants.FUNDERS_API_URL + "?query=" + request.args['q']
        elif 'id' in request.args:
            url = constants.FUNDER_WORKS_API_URL.format(request.args['id'])

    if 'page' in request.args:
        page_value = int(request.args['page'])
        offset = (page_value - 1) * constants.ROWS_PER_PAGE
        params['offset'] = str(offset)

    if 'publisher' in request.args:
        params['query.container-title'] = request.args['publisher']

    params['rows'] = str(constants.ROWS_PER_PAGE)

    return furl.furl(url).add(params)


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


def add_published_date(item, row):
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

            row['published_date'] = published_date


def add_publication(item, row):
    if "container-title" in item and len(item["container-title"]) > 0:
        container_title = item["container-title"][0]

        row['publication'] = container_title


def add_alternative_id(item, row):
    if 'alternative-id' in item:
        row['supplementary_ids'] = item['alternative-id']


def add_doi(item, row):
    if 'DOI' in item:
        row["display_doi"] = utils.get_doi_url(item['DOI'])
        row["doi"] = item['DOI']


def add_grant_info(item, row):
    if 'funder' in item:
        funders = []
        for funder in item['funder']:
            if 'name' in funder and 'award' in funder:
                funders.append(funder['name']+" ("+",".join(funder['award'])+")")
        if len(funders) > 0:
            row['grant_info'] = " | ".join(funders)


def add_names(items_list, item_name, row):
    if items_list:
        items = []
        for item in items_list:
            name = None
            if 'name' in item:
                name = item['name']
            elif 'given' in item and 'family' in item:
                name = item['given'] + " " + item['family']
            elif 'given' in item:
                name = item['given']
            if name:
                items.append(name)
        if len(items) > 0:
            row[item_name] = " | ".join(items)


def add_people(item, row):
    add_names(item['editor'] if 'editor' in item else None, 'editors', row)
    add_names(item['author'] if 'author' in item else None, 'authors', row)
    add_names(item['chair'] if 'chair' in item else None, 'chairs', row)
    add_names(item['translator'] if 'translator' in item else None, 'translators', row)


def add_supplementary_id(item, row):
    if 'alternative-id' in item:
        row['supplementary_ids'] = " | ".join(item['alternative-id'])


def add_id(item, row):
    if 'id' in item:
        row['id'] = item['id']


def add_location(item, row):
    if 'location' in item:
        row['location'] = item['location']


def add_title(item, row):
    if 'title' in item:
        row['title'] = item["title"][0].replace("\\", "") if 'title' in item else ''


def add_name(item, row):
    if 'name' in item:
        row['name'] = item['name']


def add_type(item, row):
    if "type" in item:
        item_type = item["type"]
        row['type'] = item_type.replace('-', ' ').upper()


def get_items(obj):
    items = []
    total = 0
    if obj["message"]["total-results"]:
        total = obj["message"]["total-results"]
    if obj["message"]["items"]:
        for item in obj["message"]["items"]:
            row = {}
            add_type(item, row)
            add_published_date(item, row)
            add_publication(item, row)
            add_alternative_id(item, row)
            add_title(item, row)
            add_name(item, row)
            add_id(item, row)
            add_location(item, row)
            add_doi(item, row)
            add_grant_info(item, row)
            add_people(item, row)
            add_supplementary_id(item, row)

            items.append(row)

    return items, total


def get_query_string(request, category):
    if category == constants.CATEGORY_WORKS:
        if 'q' in request.args:
            return request.args['q']

    elif category == constants.CATEGORY_FUNDERS:
        if 'id' in request.args:
            res = requests.get(constants.FUNDER_INFO_API_URL.format(request.args['id']))
            res = res.json()
            if 'message' in res:
                if 'name' in res['message']:
                    return res['message']['name']
    return ""


def search_query(category, request):
    url = get_api_url(category, request)
    res = requests.get(url)

    if res.status_code == 200:
        # items, total = get_items(core.test_data.test_result)
        # items, total = get_items(core.test_data.funder_result)
        items, total = get_items(res.json())
        page_number = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page_number, total=total, search=False, per_page=constants.ROWS_PER_PAGE,
                                href=get_pagination_url(request))
        page = {'pagination': pagination,
                'sort_url': get_request_url(request, ['sort']),
                'publisher_url': get_request_url(request, ['publisher']),
                'sort_type': sort_type(request),
                'api_url': constants.WORKS_API_URL,
                'query': get_query_string(request, category)
                }
        return items, page
