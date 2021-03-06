from PyMollom.Mollom import MollomAPI
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

mollom_api = MollomAPI(
    publicKey='6f55d167298a571801e3f6e13c6d2343',
    privateKey='43e111cebaa07bd23b00d325e31be6ce'
)


def serveCaptcha(request):
    captcha = mollom_api.getImageCaptcha(sessionID=None, authorIP="192.168.0.65")
    print captcha
    return render(request, 'mollom.html', {'captcha': captcha['url'], 'sessionID': captcha['session_id']})


@csrf_protect
def checkCaptcha(request):
    if mollom_api.checkCaptcha(sessionID=request.POST['sessionID'], solution=request.POST['answer']):
        return render(request, 'success.html')
    else:
        return render(request, 'failure.html')


def index(request):
    return render(request, 'index.html')
