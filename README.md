# Django OTP Authentication System

To Create a OTP Authentication System for Django Website

> - <a href="#validition">1. Sign Up Form Validition </a>

> - <a href="#signup">2. Create an Account With Email Verification(OTP) </a>

> - <a href="#signin">3. Sign In & Sign Out Precess With Not Verified User </a>

> - <a href="#ajax">4. Resend OTP With Ajax </a>


## 1. Sign Up Form Validition <a href="" name="validition"> - </a>

> - <a href="#jquery">I. JQuery Form Validition With Password Strength Check </a>

> - <a href="#json">II. Username & Email Validition with JsonResponse </a>


### I. JQuery Form Validition With Password Strength Check <a href="" name="jquery"> - </a>

1. Add JS file - static > js - `jquery.validate.min.js` & `jquery.passwordstrength.js`

2. Link to HTML file - templates > base > scripts.html -

   `<script type="text/javascript" src="{% static 'js/jquery.validate.min.js' %}"></script>`

   `<script type="text/javascript" src="{% static 'js/jquery.passwordstrength.js' %}"></script>`

- authentication > views.py

```python
from django.shortcuts import render
from django.views.generic import View


class SignUpView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')
```

- authentication > urls.py

```python
from .views import *
from django.urls import path


urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name="signup"),
]
```

- templates > authentication > signup.html

```html
<form id="validation-form" style="color: #757575;" method="POST">
  <div class="form-row">
    <div class="col">
      <div class="md-form">
        <input type="text" id="firstName" name="first_name" class="form-control" />
        <label for="firstName">First name</label>
      </div>
    </div>
    <div class="col">
      <div class="md-form">
        <input type="text" id="lastName" name="last_name" class="form-control" />
        <label for="lastName">Last name</label>
      </div>
    </div>
  </div>
  <div class="md-form mt-0">
    <input type="text" id="userName" name="username" class="form-control" />
    <label for="userName">Username</label>
  </div>
  <div class="md-form mt-0">
    <input type="email" id="emailField" name="email" class="form-control" />
    <label for="emailField">E-mail</label>
  </div>
  <div class="md-form">
    <input type="password" id="passwordField" name="password" class="form-control" />
    <label for="passwordField">Password</label>
  </div>
  <div class="md-form">
    <input type="password" id="confirmPassword" name="confirm_password" class="form-control" />
    <label for="confirmPassword">Re-enter password</label>
  </div>
  <div class="form-check pl-0">
    <input type="checkbox" name="agree" class="form-check-input" id="newsLetter" />
    <label class="form-check-label" for="newsLetter">Subscribe to our newsletter</label>
  </div>
  <button class="btn btn-outline-default btn-rounded btn-block my-4 waves-effect" type="submit">
    Sign Up
  </button>
  <small>By creating an account, you agree to MDB's
    <a href="" class="text-default" target="_blank">Conditions of Use</a> and
    <a href="" class="text-default" target="_blank">Privacy Notice.</a>
  </small>
  <hr />
  <p>
    Already have an account?
    <a href="" class="text-default">Sign In </a>
  </p>
</form>
```

- static > js > main.js

```javascript
$(document).ready(function () {
  $('#validation-form').validate({
    rules: {
      first_name: 'required',
      last_name: 'required',
      username: 'required',
      email: 'required',
      password: {
        required: true,
        minlength: 8,
      },
      confirm_password: {
        required: true,
        equalTo: '#passwordField',
      },
      agree: 'required',
    },
    messages: {
      first_name: 'Please enter your first name',
      last_name: 'Please enter your last name',
      username: 'Please enter a username',
      email: 'Please enter a valid email address',
      password: {
        required: 'Please provide a password',
        minlength: 'Your password must be at least 8 characters long',
      },
      confirm_password: {
        required: 'Confirm your password',
        equalTo: 'Password not match',
      },
      agree: ' ',
    },
    errorElement: 'p',
    errorPlacement: function (error, element) {
      error.addClass('invalid-feedback');

      if (element.prop('type') === 'checkbox') {
        error.insertAfter(element.next('label'));
      } else {
        error.insertAfter(element);
      }
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass('is-invalid').removeClass('is-valid');
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).addClass('is-valid').removeClass('is-invalid');
    },
  });

  // For Password Strength Check 
  if ($.fn.passwordStrength) {
    $('#passwordField').passwordStrength({
      minimumChars: 8,
    });
  }
});
```

* static > css > style.css

```css
#validation-form .progress {
  width: 100%;
  height: 5px;
  margin-top: 1rem;
  border-radius: 0;
  margin-bottom: 0.25rem;
}
#validation-form .password-score {
  font-size: 14px;
  font-weight: 700;
}
#validation-form .password-score span {
  font-size: 18px;
}
#validation-form .password-recommendation {
  font-size: 13px;
}
#validation-form .password-recommendation ul,
#validation-form .password-recommendation ol {
  padding-left: 0;
  list-style: none;
  text-decoration: none;
}
#validation-form #password-recommendation-heading {
  font-weight: 500;
  color: #0b0757;
  font-size: 14px;
  margin-bottom: 0.25rem;
}
```

### II. Username & Email Validition with JsonResponse <a href="" name="json"> - </a>

* authentication > views.py

```python
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


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
```

* authentication > urls.py

```python
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('validate_username', csrf_exempt(UsernameValidationView.as_view()), name="validate_username"),
    path('validate_email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
]
```

* templates > authentication > signup.html

```html
<div class="md-form mt-0">
 <input type="text" id="userName" name="username" class="form-control">
 <label for="userName">Username</label>
 <div class="usernameFeedBackArea invalid-feedback" style="display:none"></div>
</div>

<div class="md-form mt-0">
 <input type="email" id="emailField" name="email" class="form-control">
 <label for="email">E-mail</label>
 <div class="emailFeedBackArea invalid-feedback" style="display:none"></div>
</div>
```

* static > js > main.js

```javascript
const usernameField = document.querySelector('#userName');
const feedBackArea = document.querySelector('.usernameFeedBackArea');
const emailField = document.querySelector('#emailField');
const emailFeedBackArea = document.querySelector('.emailFeedBackArea');


usernameField.addEventListener('keyup', (e) => {
  const usernameVal = e.target.value;
  usernameField.classList.remove('is-invalid');
  feedBackArea.style.display = 'none';
  if (usernameVal.length > 0) {
    fetch('/authentication/validate_username', {
      body: JSON.stringify({ username: usernameVal }),
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          usernameField.classList.add('is-invalid');
          feedBackArea.style.display = 'block';
          feedBackArea.innerHTML = `<p style="color:#dc3545";>${data.username_error}</p>`;
        }
      });
  }
});


emailField.addEventListener('keyup', (e) => {
  const emailVal = e.target.value;
  emailField.classList.remove('is-invalid');
  emailFeedBackArea.style.display = 'none';
  if (emailVal.length > 0) {
    fetch('/authentication/validate_email', {
      body: JSON.stringify({ email: emailVal }),
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          emailField.classList.add('is-invalid');
          emailFeedBackArea.style.display = 'block';
          emailFeedBackArea.innerHTML = `<p style="color:#dc3545";>${data.email_error}</p>`;
        }
      });
  }
});
```


# 2. Create an Account With Email Verification(OTP) <a href="" name="signup"> - </a>

1. Create File > templates > authentication - `email.html` & `signin.html` | templates > partials - `_messages.html`


* sendOTP > settings.py

```python
from django.contrib import messages
from decouple import config


MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}


EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
```

* root > Create a file > .env

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=abc@example.com
DEFAULT_FROM_EMAIL=abc@example.com
EMAIL_HOST_PASSWORD=*************
EMAIL_USE_TLS=True
EMAIL_PORT=587
```

* authentication > models.py

```py
from django.db import models
from django.contrib.auth.models import User


class UserOTP(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time_st = models.DateTimeField(auto_now=True)
	otp = models.SmallIntegerField()

```

1. Run - `python manage.py makemigrations` & `python manage.py migrate`

* authentication > views.py

```python
import random
import threading
from .models import UserOTP
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


# Speed Up Email Send
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently=False)


# Sign Up View
class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'authentication/signup.html')


    def post(self, request):

        # OTP Submission
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

        # Collect Form Data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Save Form Data
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

                # Send Email Confirmation
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

# Sign In View
class SigninView(View):
    def get(self, request):
        return render(request, 'authentication/signin.html')
```

* authentication > urls.py

```python
urlpatterns = [
    path('sign_in/', SigninView.as_view(), name="signin"),
]
```

* template > authentication > signup.html

```django
<div class="col-md-6 mx-auto">
 {% include 'partials/_messages.html' %}

 {% if otp %}

 <div class="card container">
  <h5 class="card-header default-color-dark white-text text-center py-4">
   <strong>Verify Your Email</strong>
  </h5>
  <strong class="px-lg-4 pt-3 pb-1">
   To verify your email, we've sent a One Time Password (OTP) to your email address
   <a href="{% url 'signup' %}" class="text-default">(Change)</a>
  </strong>
  <div class="card-body px-lg-4 pt-4">
   <form id="validation-form" style="color: #757575;" method="POST">
    {% csrf_token %}
    <div class="md-form mt-0">
     <input type="hidden" name="user" value="{{user.username}}">
     <input type="text" id="otp" name="otp" class="form-control">
     <label for="otp">Enter OTP</label>
    </div>
    <button class="btn btn-outline-default btn-rounded btn-block my-4 waves-effect" type="submit">
     Verify Account
    </button>
    <small>
     <a href="#" class="text-default text-right">
      <i>Resend </i> OTP
     </a>
    </small>
   </form>
  </div>
 </div>

 {% else %}

 <div class="card container">
  <h5 class="card-header default-color-dark white-text text-center py-4">
   <strong>Sign up</strong>
  </h5>
  <div class="card-body px-lg-4 pt-0">
   <form id="validation-form" style="color: #757575;" method="POST">
    {% csrf_token %}
    <div class="form-row">
     <div class="col">
      <div class="md-form">
       <input type="text" id="firstName" name="first_name" class="form-control">
       <label for="firstName">First name</label>
      </div>
     </div>
     <div class="col">
      <div class="md-form">
       <input type="text" id="lastName" name="last_name" class="form-control">
       <label for="lastName">Last name</label>
      </div>
     </div>
    </div>
    <div class="md-form mt-0">
     <input type="text" id="userName" name="username" class="form-control">
     <label for="userName">Username</label>
     <div class="usernameFeedBackArea invalid-feedback" style="display:none"></div>
    </div>
    <div class="md-form mt-0">
     <input type="email" id="emailField" name="email" class="form-control">
     <label for="email">E-mail</label>
     <div class="emailFeedBackArea invalid-feedback" style="display:none"></div>
    </div>
    <div class="md-form">
     <input type="password" id="passwordField" name="password" class="form-control">
     <label for="passwordField">Password</label>
    </div>
    <div class="md-form">
     <input type="password" id="confirmPassword" name="confirm_password" class="form-control">
     <label for="confirmPassword">Re-enter password</label>
    </div>
    <div class="form-check pl-0">
     <input type="checkbox" name="agree" class="form-check-input" id="newsLetter">
     <label class="form-check-label" for="newsLetter">Subscribe to our newsletter</label>
    </div>
    <button class="btn btn-outline-default btn-rounded btn-block my-4 waves-effect" type="submit">
     Sign Up
    </button>
    <small>By creating an account, you agree to MDB's
     <a href="" class="text-default" target="_blank">Conditions of Use</a> and
     <a href="" class="text-default" target="_blank">Privacy Notice.</a>
    </small>
    <hr>
    <p>Already have an account?
     <a href="{% url 'signin' %}" class="text-default">Sign In </a>
    </p>
   </form>
  </div>
 </div>

 {% endif %}

</div>
```

* template > authentication > email.html

```django
{% load i18n %}
{% autoescape off %}

{% blocktranslate %}
You're receiving this email because you requested a otp for your user account at {{ site_name }}.
{% endblocktranslate %}

{% translate "To verify your email address, please use the following One Time Password (OTP):" %}

Your OTP is {{ otp }}

{% translate 'Do not share this OTP with anyone. Amazon takes your account security very seriously. Amazon Customer Service will never ask you to disclose or verify your Amazon password, OTP, credit card, or banking account number. If you receive a suspicious email with a link to update your account information, do not click on the link—instead, report the email to Amazon for investigation.' %}

{% translate "Thank you for shopping with us! We hope to see you again soon." %}

{% blocktranslate %}The {{ site_name }} team{% endblocktranslate %}

{% endautoescape %}
```

* template > partials > _messages.html

```django
{% if messages %}
<div class="messages">
  {% for message in messages %}
  <div {% if message.tags %} class="alert alert-sm alert-{{ message.tags }}" {% endif %}>
    {{ message }}
  </div>
  {% endfor %}
</div>
{% endif %}
```


# 3. Sign In & Sign Out Precess With Not Verified User <a href="" name="signin"> - </a>

* authentication > views.py

```python
from django.contrib.auth import authenticate, login, logout

# Sign In Vier
class SigninView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'authentication/signin.html')
    
    def post(self, request):

        # OTP Submission
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
            
            # Send Mail
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

# Sign Out View
def signoutView(request):
    logout(request)
    messages.success(request, 'You are sign out successfully')
    return redirect('signin')

```

- authentication > urls.py

```python
urlpatterns = [
    path('sign_out/', signoutView, name="signout"),
]
```

* templates > authentication > signin.html

```django
<div class="col-md-6 mx-auto">
 {% include 'partials/_messages.html' %}

 {% if otp %}

 <div class="card container">
  <h5 class="card-header default-color-dark white-text text-center py-4">
   <strong>Verify Your Email</strong>
  </h5>
  <strong class="px-lg-4 pt-3 pb-1">To verify your email, we've sent a One Time Password (OTP) to your email address
   <a href="{% url 'signup' %}" class="text-default">(Change)</a>
  </strong>
  <div class="card-body px-lg-4 pt-4">
   <form id="validation-form" style="color: #757575;" action="" method="POST">
    {% csrf_token %}
    <div class="md-form mt-0">
     <input type="hidden" name="user" value="{{user.username}}">
     <input type="text" id="otp" name="otp" class="form-control">
     <label for="userName">OTP</label>
    </div>
    <button class="btn btn-outline-default btn-rounded btn-block my-4 waves-effect" type="submit">
     Verify Account
    </button>
    <small>
     <a href="#" class="text-default text-right">
      <i>Resend </i> OTP
     </a>
    </small>
   </form>
  </div>
 </div>

 {% else %}

 <div class="card container">
  <h5 class="card-header default-color-dark white-text text-center py-4">
   <strong>Sign In</strong>
  </h5>
  <div class="card-body px-lg-4 pt-4">
   <form id="validation-form" style="color: #757575;" action="" method="POST">
    {% csrf_token %}
    <div class="md-form mt-0">
     <input type="text" id="userName" name="username" class="form-control">
     <label for="userName">Username</label>
    </div>
    <div class="md-form">
     <input type="password" id="password" name="password" class="form-control">
     <label for="password">Password</label>
    </div>
    <div class="form-check pl-0">
     <input type="checkbox" class="form-check-input" id="keepMe">
     <label class="form-check-label" for="keepMe">Keep me sign in</label>
    </div>
    <button class="btn btn-outline-default btn-rounded btn-block my-4 waves-effect" type="submit">Sign In</button>
    <small>
     <a href="" class="text-default">Forgot password?</a>
    </small>
    <hr>
    <p>Not a member?
     <a href="{% url 'signup' %}" class="text-default">Sign Up </a>
    </p>
   </form>
  </div>
 </div>

 {% endif %}

</div>
```


* templates > partials > _header.html

```django
{% if request.user.is_authenticated %}
  <a href="{% url 'signout' %}"> Sign Out </a>
{% else %}
  <a href="{% url 'signin' %}">Sign In</a>
{% endif %}
```

# 4. Resend OTP With Ajax <a href="" name="ajax"> - </a>

* authentication > views.py

```python
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
```


* authentication > urls.py

```python
urlpatterns = [
    path('resendOTP', ResendOTP.as_view()),
]
```

* static > js > main.ja

```js
function ReSendOTP(username, mess_id) {
  mess = document.getElementById(mess_id);
  mess.innerText = 'Sending...';
  $.ajax({
    type: 'GET',
    url: '/authentication/resendOTP',
    data: { user: username },
    success: function (data) {
      mess.innerText = data;
    },
  });
}
```

* templates > authentication > signin.html & signup.html

```html
{% if otp %}

<small>
 <a href="#" class="text-default text-right" onclick="ReSendOTP('{{user.username}}', 'resendOTPmess')">
  <i id="resendOTPmess">Resend </i> OTP
 </a>
</small>

{% else %}


{% endif %}
```


## Getting started

Steps:

1. Clone/pull/download this repository
2. Create a virtualenv with `virtualenv venv` and install dependencies with `pip install -r requirements.txt`
3. Configure your .env variables
4. Rename your project with `python manage.py rename <yourprojectname> <newprojectname>`
5. Collect all static files `python manage.py collectstatic`

This project includes:

1. Validation Form with Jquery
2. OTP send with email
3. Resend OTP
