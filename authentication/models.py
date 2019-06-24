from django.contrib.auth.models import User
from django.db import models

# @TODO: support multiple login source
# class SocialMediaApp(models.Model):
#
#     media_type = models.CharField(choices=)
#
#     app_id = models.CharField()
#
#     app_secret_key = models.CharField()


class OauthUser(models.Model):
    # @TODO: support multiple login source
    # app = models.ForeignKey(SocialMediaApp, on_delete=models.SET_NULL)

    external_id = models.CharField(max_length=150, db_index=True)

    profile_picture = models.CharField(max_length=1024)

    access_token = models.CharField(max_length=150)

    token_expires_in = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        app_label = 'authentication'
        db_table = 'authentication_oauth_users'
        default_permissions = ('add', 'change', 'delete')
