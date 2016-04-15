## Tady se nastavuje, co všechno z naší aplikace bude vidět
## v administračním rozhraní.
## Aby se tam dalo měnit všechno, registrujeme všechny modely
## z models.py.

from django.contrib import admin
from voting import models

# Register your models here.
admin.site.register(models.Poll)
admin.site.register(models.Option)
admin.site.register(models.Record)
admin.site.register(models.Vote)
