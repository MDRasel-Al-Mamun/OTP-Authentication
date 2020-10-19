import json
import random
import threading
from .models import UserOTP
from django.conf import settings
from django.core.mail import EmailMessage
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username is already taken, choose another one'}, status=409)
        if len(username) < 8:
            return JsonResponse({'username_error': 'Your username must consist of at least 8 characters'}, status=400)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, email is already taken, choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'authentication/signup.html')

    def post(self, request):

        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)
            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                messages.success(request, f'Account is Created For {user.username}')
                return redirect('signin')
            else:
                messages.warning(request, f'You Entered a Wrong OTP')
                return render(request, 'authentication/signup.html', {'otp': True, 'user': user})

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    return render(request, 'authentication/signup.html')
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = False
                user.save()

                user_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user=user, otp=user_otp)
                current_site = get_current_site(self.request)
                email_subject = 'Welcome to MDB - Verify Your Email'
                email_body = render_to_string('authentication/email.html', {
                    'user': user,
                    'site_name': current_site.name,
                    'otp': user_otp,
                })
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                EmailThread(email).start()
                return render(request, 'authentication/signup.html', {'otp': True, 'user': user})
        return render(request, 'authentication/signup.html')


class ResendOTP(View):
    def get(self, request):
        get_user = request.GET['user']
        if User.objects.filter(username=get_user).exists() and not User.objects.get(username=get_user).is_active:
            user = User.objects.get(username=get_user)

            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            current_site = get_current_site(self.request)
            email_subject = 'Welcome to MDB - Verify Your Email'
            email_body = render_to_string('authentication/email.html', {
                'user': user,
                'site_name': current_site.name,
                'otp': user_otp,
            })
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            EmailThread(email).start()
            return HttpResponse("Resend")
        return HttpResponse("Can't Send ")


class SigninView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'authentication/signin.html')
    
    def post(self, request):

        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)
            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, f'You Entered a Wrong OTP')
                return render(request, 'authentication/signup.html', {'otp': True, 'user': user})

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        elif not User.objects.filter(username=username).exists():
            messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('signin')
        
        elif not User.objects.get(username=username).is_active:
            user = User.objects.get(username=username)

            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            current_site = get_current_site(self.request)
            email_subject = 'Welcome to MDB - Verify Your Email'
            email_body = render_to_string('authentication/email.html', {
                'user': user,
                'site_name': current_site.name,
                'otp': user_otp,
            })
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            EmailThread(email).start()
            return render(request, 'authentication/signin.html', {'otp': True, 'user': user})
        
        else:
            messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('signin')
        return render(request, 'authentication/signin.html')


def signoutView(request):
    logout(request)
    messages.success(request, 'You are sign out successfully')
    return redirect('signin')
