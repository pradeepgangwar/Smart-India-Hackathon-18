from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            user.username = email.split('@')[0]
            # password = id_generator()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'sih/base.html', )
    else:
        form = UserForm()

    return render(request, 'sih/signup.html', {'form': form})

def logout(request):
    logout(request)

    return render(request, 'sih/base.html')

def index(request):
    return render(request, 'sih/base.html')