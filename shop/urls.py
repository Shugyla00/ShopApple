from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    # path('', cache_page(60)(IndexView.as_view()), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/', CartPageView.as_view(), name="cart"),
    path('buy/cart/items/', bylAllInCart, name="buyCartItems"),
    path('update/user/money/', updateUserMoney, name="updateUserMoney"),
    path('category/<slug:slug>/', CategoryView.as_view(), name="category"),
    path('<slug:cat_slug>/<slug:slug>', ShowView.as_view(), name='item_show'),
    path('auth/register/', Register.as_view(), name="authRegister"),
    path('auth/login/', LoginUserForm.as_view(), name="authLogin"),
    path('auth/logout/', my_logout, name="authLogout"),
]
