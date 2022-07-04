from django.urls import path
from . views import Users, Products

app_name = 'api'

urlpatterns = [
    path('users/', Users.as_view()),
    path('products/', Products.as_view()),
]