from django.contrib import admin
from django.db import models

# Register your models here.
from pagedown.widgets import AdminPagedownWidget
from shops.models import Service, ShopAccount

class ShopAccountAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

admin.site.register(Service)
admin.site.register(ShopAccount, ShopAccountAdmin)