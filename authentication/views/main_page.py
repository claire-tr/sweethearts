from django.contrib.auth.decorators import login_required


@login_required
def main_page(request, template_name='main_page.html'):
    """
    main page of the app, display the user information
    :param request:
    :param template_name:
    :return:
    """
    pass