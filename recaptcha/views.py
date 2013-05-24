from recaptcha.client import captcha
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


publicKey = '6Lf98eASAAAAAMARWX5AXv33iiHwS6E6I3tkVOFT'
privateKey = '6Lf98eASAAAAALOFfNYMQEROO1VqJ9tjbHM9DuB9'


def serveCaptcha(request):
    html = captcha.displayhtml(publicKey)
    return render(request, 'recaptcha.html', {'captcha': html})


@csrf_protect
def checkCaptcha(request):
    check = captcha.submit( request.POST['recaptcha_challenge_field'],
                            request.POST['recaptcha_response_field'],
                            privateKey,
                            '192.168.1.1')
    if check.is_valid:
        return render(request, 'success.html')
    else:
        return render(request, 'failure.html') 