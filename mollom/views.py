from PyMollom.Mollom import MollomAPI
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

mollom_api = MollomAPI(
    publicKey='6f55d167298a571801e3f6e13c6d2343',
    privateKey='43e111cebaa07bd23b00d325e31be6ce'
)


def serveCaptcha(request):
    return render(request, 'mollom.html')


@csrf_protect
def checkIfSpam(request):
    data = request.POST
    spam = (mollom_api.checkContent(authorName=data['username'], postBody=data['body']))['spam']
    if(spam == 1):    # No es spam
        resp = HttpResponse("ham", content_type="text/plain")
    elif(spam == 2):  # Es spam
        resp = HttpResponse("spam", content_type="text/plain")
    elif(spam == 3):  # No es seguro que sea spam
        captcha = mollom_api.getImageCaptcha(sessionID=None, authorIP=request.META['REMOTE_ADDR'])
        resp = HttpResponse(captcha['url'], content_type="text/plain")
    return resp


@csrf_protect
def checkCaptcha(request):
    if mollom_api.checkCaptcha(sessionID=request.POST['sessionID'], solution=request.POST['answer']):
        resp = render(request, 'success.html')
    else:
        resp = render(request, 'failure.html')
    return resp


def index(request):
    return render(request, 'index.html')
