from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, redirect
from django.urls import reverse_lazy

from firstsite import settings
from logo.models import ScriptPost
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm

# Create your views here.


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users_temps/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and self.request.user.is_authenticated:
            return next_url
        else:
            return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users_temps/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {
        'title': "Регистрация"
    }

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user_group = Group.objects.get(name='DefaultUser')
            user.groups.add(user_group)

            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users_temps/profile.html'
    extra_context = {
        'title': 'Профиль пользователя',
        'default_image': settings.DEFAULT_USER_IMAGE
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = 'users_temps/password_change_form.html'
    extra_context = {'title': 'Изменение пароля'}
