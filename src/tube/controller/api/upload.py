from flask import request
from http_client import HttpClient
from app import flask, controller
from pyboot.json import json_response
from conf import Conf
import pafy
import os
import re
import wget
from urllib.parse import urlparse, parse_qs
from pyboot.exception import InvalidValueException

hosts = Conf.get('hosts')
self_host = hosts['self']
api_host = Conf.get('api_host')


@flask.route('/video', methods=["GET"])
@controller.api_controller()
def get_video_link():
    url = request.args['url']
    video_id = extract_video_id(url)

    r = HttpClient().get(url=api_host + '/api/searchVideo?key=' + video_id)
    r = r.json()
    for file in r:
        if file['host'] == self_host:
            return json_response(file_url(video_id))

    for file in r:
        if is_video_available_on_host(file['host'], video_id):
            return json_response(file_url(video_id))

    location = download_video(url)
    HttpClient().get(url=api_host + '/api/addVideo?key=' + video_id + '&host=' + str(
        self_host) + '&location=' + location)

    return json_response(file_url(video_id))


def is_video_available_on_host(host_id, video_id):
    # file_name = wget.download(file_url, out=os.path.abspath("../public"))
    return False


def download_video(url):
    video = pafy.new(url)
    best = video.getbest()
    filename = best.download(filepath=os.path.abspath("../public"))
    os.rename(filename, os.path.abspath("../public") + '/' + video.videoid)
    return os.path.abspath("../public") + '/' + video.videoid


def file_url(video_id):
    return {'url': 'http://localhost:5000/static/' + video_id}


def extract_video_id(url):
    """ Extract the video id from a url, return video id as str. """
    idregx = re.compile(r'[\w-]{11}$')
    url = str(url)

    if idregx.match(url):
        return url  # ID of video

    if '://' not in url:
        url = '//' + url
    parsedurl = urlparse(url)
    if parsedurl.netloc in ('youtube.com', 'www.youtube.com', 'm.youtube.com', 'gaming.youtube.com'):
        query = parse_qs(parsedurl.query)
        if 'v' in query and idregx.match(query['v'][0]):
            return query['v'][0]
    elif parsedurl.netloc in ('youtu.be', 'www.youtu.be'):
        vidid = parsedurl.path.split('/')[-1] if parsedurl.path else ''
        if idregx.match(vidid):
            return vidid

    err = "Need 11 character video id or the URL of the video. Got %s"
    raise InvalidValueException(err % url)
