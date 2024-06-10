from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import City, Address, Lesson, Module, Course, PayType, Payment


class AddressView(View):
    def get(self, request):
        city = City.objects.all()
        address = Address.objects.all()
        context = {
            "cities": city,
            "addresses": address
        }
        return render(request, "address.html", context)


class LoginPageView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        data = {
            "username": username,
            "password": password
        }
        login_form = AuthenticationForm(data=data)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            return redirect("landing")
        else:

            context = {
                "form": login_form,
            }
            return render(request, "login.html", context)


class RegisterPageView(View):

    def get(self, request):
        form = UserRegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request):
        create_form = UserRegisterForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('login')

        else:
            context = {'form': create_form}
            return render(request, 'register.html', context)


class LessonPageView(LoginRequiredMixin, View):
    def get(self, request):
        lessons = Lesson.objects.all()
        modules = Module.objects.all()
        courses = Course.objects.all()
        context = {'lessons': lessons,
                   'modules': modules,
                   'courses': courses
                   }
        return render(request, 'course.html', context)


class PayPageView(LoginRequiredMixin, View):
    def get(self, request):
        pyt = PayType.objects.all()
        payment = Payment.objects.all()
        context = {'pyts': pyt, 'payments': payment}
        return render(request, 'payments.html', context)


class LogoutPageView(View):
    def get(self, request):
        logout(request)
        return redirect('landing')

