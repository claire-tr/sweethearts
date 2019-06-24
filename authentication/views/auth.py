from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='login.html'):
    """
    Overrides Django's default login to check for first time login
    Displays the FB login button to send oauth request
    :param request:
    :param template_name:
    :return:
    """
    pass