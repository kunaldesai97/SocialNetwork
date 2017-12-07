from django.contrib import admin
from .models import Person, Friends, Profile
# Register your models here.

admin.site.register(Person)
admin.site.register(Friends)
admin.site.register(Profile)