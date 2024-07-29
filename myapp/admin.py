from django.contrib import admin
from myapp.models import CustomUser, Movie, Rating

admin.site.register(CustomUser)
admin.site.register(Movie)
admin.site.register(Rating)