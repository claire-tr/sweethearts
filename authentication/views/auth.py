from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

from authentication.views import main_page
from authentication.helpers.facebook_oauth_helpr import oauth_login_url


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_page(request, template_name='login.html'):
    """
    Overrides Django's default login to check for first time login
    Displays the FB login button to send oauth request
    :param request:
    :param template_name:
    :return:
    """
    if not request.user.is_anonymous:
        return redirect(main_page)
    context = {
        'facebook_oauth_url': oauth_login_url()
    }
    return TemplateResponse(request, template_name, context)
