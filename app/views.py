from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import City, Address, Lesson, Module, Course, PayType, Payment
from werkzeug.security import check_password_hash
from django.contrib.auth.hashers import check_password


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

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                return redirect("landing")
            else:
                context = {
                    "error": "Invalid username or password"
                }
                return render(request, "login.html", context)
        except User.DoesNotExist:
            context = {
                "error": "Invalid username or password"
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

