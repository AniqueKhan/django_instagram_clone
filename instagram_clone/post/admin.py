from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Post)
admin.site.register(models.Tag)
admin.site.register(models.Follow)
admin.site.register(models.Stream)
