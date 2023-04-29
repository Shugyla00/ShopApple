from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from .forms import RegisterForm, UpdateUserForm
from .models import *
from .serializers import UserSerializer, ItemSerializer, CategorySerializer
from .utils import DataMixin


def index(request):
    items = Item.objects.all()
    return render(request, 'shop/index.html', {'items': items, 'title': 'Главная страница'})


def about(request):
    return render(request, 'shop/about.html', {'title': 'О сайте'})


def categories(request):
    pass


def pageNotFound(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# =========================================== class controllers

class IndexView(DataMixin, ListView):
    paginate_by = 3
    model = Item
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="apps page")
        return dict(list(context.items()) + list(mixin.items()))

    def get_queryset(self):
        return Item.objects.select_related("category")


class AboutView(DataMixin, TemplateView):
    template_name = "shop/about.html"

    def get_context_data(self, **kwargs):
        return self.get_user_context(title="about page")


class ShowView(DataMixin, DetailView):
    model = Item
    template_name = "shop/item/show.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="show page")
        return dict(list(context.items()) + list(mixin.items()))

    def post(self, request, **kwargs):
        my_data = request.POST
        user = request.user
        newOrder = Order()
        newOrder.user = user
        newOrder.item = Item.objects.get(pk=my_data.get("item_id", None))
        newOrder.save()
        return redirect('cart')


class CategoryView(DataMixin, DetailView):
    model = Category
    template_name = "shop/item/category.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        activities = self.get_related_activities()
        context['related_activities'] = activities
        context['page_obj'] = activities
        mixin = self.get_user_context(title="category page")
        return dict(list(context.items()) + list(mixin.items()))

    def get_related_activities(self):
        queryset = self.object.item_set.all()
        paginator = Paginator(queryset, 3)
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


class Register(DataMixin, CreateView):
    pass
    form_class = RegisterForm
    template_name = "shop/register.html"
    success_url = reverse_lazy('home')

    # login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="register page")
        return dict(list(context.items()) + list(mixin.items()))


class LoginUserForm(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'shop/login.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="login page")
        return dict(list(context.items()) + list(mixin.items()))


class ProfileView(DataMixin, TemplateView):
    template_name = "shop/profile.html"
    form = UpdateUserForm

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"]:
            print(request.POST)
            form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
        return redirect('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form(instance=self.request.user)
        mixin = self.get_user_context(title="profile page")
        return dict(list(context.items()) + list(mixin.items()))


class CartPageView(DataMixin, ListView):
    template_name = "shop/cart.html"
    model = Order

    def get_queryset(self):
        user = self.request.user
        q = Order.objects.select_related("user").select_related("item").filter(user=user, isOrdered=False).all()
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.get_user_context(title="profile page")
        return dict(list(context.items()) + list(mixin.items()))

    def post(self, request, **kwargs):
        order = request.POST.get("cart_id", None)
        if order:
            Order.objects.get(pk=order).delete()
            messages.error(request, "item successfully deleted in cart.")
        else:
            return HttpResponseNotFound

        return redirect('cart')


@login_required
def my_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def bylAllInCart(request):
    if request.method == "POST":
        userItems = Order.objects.select_related("item").filter(user=request.user, isOrdered=False).all()
        itemsMoney = 0
        for i in userItems:
            itemsMoney += i.item.money
        if request.user.money > itemsMoney:
            Order.objects.filter(user=request.user, isOrdered=False).all().order_by('item').update(isOrdered=True)
            request.user.money = request.user.money - itemsMoney
            request.user.save()
        else:
            messages.error(request, "no money.")
            return redirect('cart')
        messages.info(request, "You have successfully buys items.")
        return redirect('profile')


def updateUserMoney(request):
    if request.method == "POST":
        req = request.POST.get("money", None)
        if req is not None:
            request.user.money = request.user.money + int(req)
            request.user.save()
        return redirect('profile')


class Pagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.action == 'post' or self.action == 'put' or self.action == 'delete':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = Pagination


class PaginationItemsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]
    pagination_class = Pagination