from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('<slug:cat_slug>/<slug:slug>', ShowView.as_view(), name='item_show'),
    path('register', Register.as_view(), name="register"),
    path('login', LoginUserForm.as_view(), name="login"),
    path('logout', my_logout, name="logout"),
]
