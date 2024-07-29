from . import views
from django.urls import path
urlpatterns = [
    path('admin', views.index_page, name='index_page'),
    path('add/', views.add_view, name='add_view'),
    path('', views.page, name='page'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('insert_ratings/', views.insert_ratings, name='insert_ratings'),
    # Movie management
    path('insert_movie/', views.insert_movie, name='insert_movie'),
    path('update_movie/', views.update_movie, name='update_movie'),
    path('delete_movie/', views.delete_movie, name='delete_movie'),

    # User management
    path('insert_user/', views.insert_user, name='insert_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/', views.delete_user, name='delete_user'),

    # Rating management
    path('insert_rating/', views.insert_rating, name='insert_rating'),
    path('update_rating/', views.update_rating, name='update_rating'),
    path('delete_rating/', views.delete_rating, name='delete_rating'),
]