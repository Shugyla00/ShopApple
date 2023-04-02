from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView

from .forms import RegisterForm
from .models import *
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


@login_required
def my_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")
