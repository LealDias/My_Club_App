from django.contrib import admin

# Register your models here.

# Import the Models
from .models import Venue
from. models import MyClubUser
from. models import Event

# Register the Models

admin.site.register(Venue)
admin.site.register(MyClubUser)
admin.site.register(Event)

