import logging

from flask import url_for

# from common.client.statsd_client import StatsdClient
from conf import Conf
from urllib.parse import urlparse


def get_next_url(request):
    if is_next_url(request):
        return request.args.get("next")
    else:
        return "http://" + Conf.get("app_host") + url_for("home_page_pms")


def is_next_url(request):
    return "next" in request.args


def get_url(url, request):
    if is_next_url(request):
        return url + "?next=" + request.args.get("next")
    else:
        return url


def get_query_string(request):
    parse_object = urlparse(request.url)
    query_params = ""
    if len(parse_object.query) > 0:
        query_params = "?" + parse_object.query
    return query_params


def get_path(request):
    parse_object = urlparse(request.url)
    return parse_object.path
