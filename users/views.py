from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'login':

            email = request.POST.get('email', '').strip().lower()
            password = request.POST.get('password')
            remember = request.POST.get('remember')

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:

                login(request, user)

                if remember:
                    request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    request.session.set_expiry(0)

                messages.success(request, 'Login successful.')

                return redirect('users:dashboard')

            else:

                messages.error(
                    request,
                    'Invalid email or password.',
                    extra_tags='login'
                )

        elif action == 'register':

            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip().lower()
            password = request.POST.get('password')
            terms = request.POST.get('terms')

            if not full_name or not email or not password:

                messages.error(
                    request,
                    'Please complete all fields.',
                    extra_tags='register'
                )

            elif not terms:

                messages.error(
                    request,
                    'Please agree to the Terms of Service and Privacy Policy.',
                    extra_tags='register'
                )

            elif len(password) < 8:

                messages.error(
                    request,
                    'Password must have at least 8 characters.',
                    extra_tags='register'
                )

            elif User.objects.filter(username=email).exists():

                messages.error(
                    request,
                    'This email is already registered.',
                    extra_tags='register'
                )

            else:

                name_parts = full_name.split()

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name_parts[0],
                    last_name=' '.join(name_parts[1:])
                )

                login(request, user)

                messages.success(request, 'Account created successfully.')

                return redirect('users:index')

    return render(request, 'users/index.html')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')
                  
