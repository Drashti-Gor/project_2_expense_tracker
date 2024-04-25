from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from .forms import UserCreateForm, LoginForm1
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

def login_view(request):
    if request.method == 'POST':
        form = LoginForm1(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username,password=password)
            if user:
                login(request, user)
                return redirect(reverse('expense:home') )
            else:
                messages.error(request, "Invalid Credentials!")
                return redirect('users:login')


    else:
        form  = LoginForm1()
        return render(request, 'users/login.html', {'form': form})
    
# @login_required
def logout1(request):
    print('Got control')
    logout(request)
    # messages.error(request, "logged out!")
    return render(request, 'users/logout.html')




