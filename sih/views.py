from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('base.html')
    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form, 'status':'logged_in'})

def logout(request):
    logout(request)

    return HttpResponseRedirect('signup.html')

def index(request):
    return HttpResponseRedirect('base.html')