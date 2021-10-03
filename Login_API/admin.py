from django.contrib import admin
from .models import *
# Register your models here.


class OneTimePassAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp', 'dat_created']
    search_fields = ['user__username', 'otp']
admin.site.register(OneTimePass, OneTimePassAdmin)
