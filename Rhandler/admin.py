from django.contrib import admin
from Rhandler import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Client)
admin.site.register(models.Message)
