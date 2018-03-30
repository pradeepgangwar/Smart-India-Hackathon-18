from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.files.storage import FileSystemStorage

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

def profile(request):
    form = None
    Elementry = 'Elementry'
    HighSchool =  'High School'
    SeniorSecondary = 'Secondary Education'
    Undergraduate = 'Undergraduate'
    Postgraduate = 'Postgraduate'
    Doctorate = 'Doctoral Degree'

    QUALIFICATIONS = (
        (Elementry, Elementry),
        (HighSchool,  HighSchool),
        (SeniorSecondary, SeniorSecondary),
        (Undergraduate, Undergraduate),
        (Postgraduate, Postgraduate),
        (Doctorate, Doctorate),
    )

    Male = 'Male'
    Female =  'Female'
    Others = 'Others'
    
    GENDER = (
        (Male, Male),
        (Female,  Female),
        (Others, Others),
    )
    if request.method=="POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            print (1)
            age = form.cleaned_data['age']
            gender = request.POST.get('gender')
            qualification = request.POST.get('qualification')
            resume = request.FILES['resume']
            profilepicture = request.FILES['profilepicture']
            fs = FileSystemStorage()
            filename_resume = fs.save(resume.name, resume)
            uploaded_resume_url = fs.url(filename_resume)

            filename_profilepicture = fs.save(profilepicture.name, profilepicture)
            uploaded_profilepicture_url = fs.url(filename_profilepicture)

            is_subscribed = True
            user = User.objects.get(username=request.user.username)

            Profile = UserProfile.objects.create(user=user,age=age,gender=gender,resume=resume,profilepicture=profilepicture,is_subscribed=is_subscribed,qualification=qualification)
            Profile.save()

            return render(request, 'sih/profile.html', {
                'uploaded_resume_url': uploaded_resume_url,
                'uploaded_profilepicture_url': uploaded_profilepicture_url,
                'qualifications_choices':QUALIFICATIONS,
                'age_choices':GENDER
            })

    else:
        form = UserProfileForm()

    return render(request, 'sih/profile.html', {'form': form, 'status':'logged_in','qualifications_choices':QUALIFICATIONS,'age_choices':GENDER})
