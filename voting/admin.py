from django.contrib import admin
from voting import models

# Register your models here.
admin.site.register(models.Poll)
admin.site.register(models.Option)
admin.site.register(models.Record)
admin.site.register(models.Vote)
