import logging
from django.contrib.auth import login
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from authentication.views import main_page
from authentication.views.auth import login_page
from authentication.helpers import FacebookOauthHelper


@transaction.atomic
def facebook_auth_callback(request):
    """
    callback for facebook authorization
    :param request:
    :return:
    """
    try:
        user = FacebookOauthHelper(request.GET.dict()).authorize()
        login(request, user)
    except ValueError as e:
        logging.error('login failed: %s' % e)
        return redirect(login_page)
    return redirect(main_page)


@transaction.atomic
def facebook_de_auth_callback(request):
    """
    call back method when user removes this app
    :param request:
    :return:
    """
    try:
        FacebookOauthHelper(request.POST.dict()).de_auth()
    except ValueError as e:
        return HttpResponse(status=400, content='DeAuth failed: %e' % e)

    return HttpResponse(status=204, content='DeAuth Succeed.')
