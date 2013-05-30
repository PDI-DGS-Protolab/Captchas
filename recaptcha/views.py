from recaptcha.client import captcha
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


publicKey = '6LfFEeISAAAAACxEsljeHqJh-9x57e4fhlosHKeP'
privateKey = '6LfFEeISAAAAAC1KZ4LTLekta9DctMPnKZS1nAQQ'


def serveCaptcha(request):
    html = captcha.displayhtml(publicKey)
    return render(request, 'recaptcha.html', {'captcha': html})


@csrf_protect
def checkCaptcha(request):
    check = captcha.submit( request.POST['recaptcha_challenge_field'],
                            request.POST['recaptcha_response_field'],
                            privateKey,
                            request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR'))
    if check.is_valid:
        return render(request, 'success.html')
    else:
        return render(request, 'failure.html')
