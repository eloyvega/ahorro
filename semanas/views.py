import datetime
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
        cantidades = Semana.objects.values_list('cantidad', flat=True).filter(usuario=request.user)
        if len(cantidades) < 52:
            cantidades = [cantidad / 10 for cantidad in cantidades]
            nueva_cantidad = random.choice([number for number in range(1, 53) if number not in cantidades])
            semana = Semana()
            semana.numero = len(cantidades) + 1
            semana.cantidad = nueva_cantidad * 10
            semana.usuario = request.user
            semana.fecha = self.get_fecha(semana.numero - 1)
            semana.save()
        return HttpResponseRedirect(reverse('home'))

    @staticmethod
    def get_fecha(numero):
        fecha_base = datetime.date(2016, 1, 3)
        return fecha_base + datetime.timedelta(7 * numero)
