from PyMollom.Mollom import MollomAPI
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads, dumps

mollom_api = MollomAPI(
    publicKey='6f55d167298a571801e3f6e13c6d2343',
    privateKey='43e111cebaa07bd23b00d325e31be6ce'
)


def serveCaptcha(request):
    return render(request, 'mollom.html')


@csrf_exempt
def checkIfSpam(request):
    json = request.raw_post_data
    data = loads(json)
    spam = (mollom_api.checkContent(authorName=data['user'], postBody=data['comment']))['spam']

    if spam == 1:    # No es spam
        res = {'status': 'ham', 'url': '/success'}

    elif spam == 2:  # Es spam
        res = {'status': 'spam', 'url': '/failure'}

    elif spam == 3:  # No es seguro que sea spam
        author = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        captcha = mollom_api.getImageCaptcha(sessionID=None, authorIP=author)
        res = {'status': 'notSure', 'url': captcha['url'], 'session_id': captcha['session_id']}

    else:
        res = {}

    json = dumps(res)
    resp = HttpResponse(json, content_type="text/json")
    return resp


@csrf_exempt
def checkCaptcha(request):
    json = request.raw_post_data
    data = loads(json)

    if mollom_api.checkCaptcha(sessionID=data['session_id'], solution=data['answer']):
        res = {'status': 'success', 'url': '/success'}
    else:
        res = {'status': 'failure', 'url': '/failure'}

    json = dumps(res)
    resp = HttpResponse(json, content_type="text/json")
    return resp


def index(request):
    return render(request, 'index.html')


def success(request):
    return render(request, 'success.html')


def failure(request):
    return render(request, 'failure.html')
