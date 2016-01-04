import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, RedirectView

from .mixins import LoginRequiredMixin, AnonymousRequiredMixin
from .models import Semana


class SigninView(AnonymousRequiredMixin, View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'semanas/signin.html', {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Inactive user.')
        else:
            form = AuthenticationForm()
            return render(request, 'semanas/signin.html', {
                'form': form,
                'error_message': 'Usuario o contraseña incorrecto',
            })


class SignoutView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self):
        logout(self.request)
        return reverse('home')


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        semanas = Semana.objects.filter(usuario=request.user).order_by('numero')
        return render(request, 'semanas/home.html', {'semanas': semanas})

    def post(self, request):
        semanas = Semana.objects.filter(usuario=request.user)
        l = []
        for semana in semanas:
            l.append(semana.cantidad / 10)
        cantidad = random.choice(list(set(range(1, 53)) - set(l)))
        nuevo = Semana()
        nuevo.numero = semanas.count() + 1
        nuevo.cantidad = cantidad * 10
        nuevo.usuario = request.user
        nuevo.save()
        return HttpResponseRedirect(reverse('home'))
