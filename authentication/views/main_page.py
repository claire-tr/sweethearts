from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


@login_required
def main_page(request, template_name='main_page.html'):
    """
    main page of the app, display the user information
    :param request:
    :param template_name:
    :return:
    """
    context = {
        'user': request.user,
        'profile_pic': request.user.oauthuser_set.get().profile_picture
    }
    return TemplateResponse(request, template_name, context)
