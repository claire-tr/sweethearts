from django.conf.urls import url

from authentication.views import login_page, main_page, facebook_auth_callback, facebook_de_auth_callback

urlpatterns = [
    url(r'^$', main_page),
    url(r'^login/', login_page),
    url(r'^oauth/facebook/authorize', facebook_auth_callback),
    url(r'^oauth/facebook/de-auth', facebook_de_auth_callback),
]
