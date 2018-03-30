from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm, Vacancy,Applications,Query
from django.contrib.auth.models import User
from .models import UserProfile, vacancy, DeptProfile, applications,query,notifications, activation
from django.core.files.storage import FileSystemStorage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import os

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            to_email = []
            user = form.save(commit=False)
            user.is_active = False
            email = form.cleaned_data['email']
            user.username = email.split('@')[0]
            user.set_password(form.cleaned_data['password'])
            mail_subject = 'Activate your blog account.'
            to = str(form.cleaned_data['email'])
            to_email.append(to)
            user.save()
            uid = str(user.pk)
            token = str(account_activation_token.make_token(user))
            username = str(user.username)
            from_email = 'pradeepgangwar39@gmail.com'
            message = "Hi "+username+" Please click on the link to confirm your registration, http://localhost:8000/activate?email="+to+"&token="+token+"&uid="+uid
            send_mail(
                mail_subject,
                message,
                from_email,
                to_email,
            )
            act = activation.objects.create(user=user, email=to, token=token)
            act.save()
            return redirect('http://localhost:8000/accounts/login/')
    else:
        form = UserForm()
        
    return render(request, 'sih/signup.html', {'form': form})

def activate(request):
    email = request.GET['email']
    token = request.GET['token']
    uid = request.GET['uid']
    user = User.objects.get(id=uid)
    act = activation.objects.filter(email=email, token=token, user=user)

    if act is not None:
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def logout(request):
    logout(request)

    return render(request, 'sih/base.html')

def index(request):
    # user_id = request.user
    request.session['username'] = request.user.username
    dept_result = None
    vacancy_result  = None
    all = True
    if request.method=="POST":
        search = request.POST.get('search')
        dept_result = DeptProfile.objects.filter(dept_name=search)
        vacancy_result = vacancy.objects.filter(title=vacancy_result)
        all = False

    else:
        dept_result = DeptProfile.objects.filter()
        vacancy_result = vacancy.objects.filter()
        
    return render(request, 'sih/index.html',{'dept_result':dept_result,'vacancy_result':vacancy_result,'all':all})


@login_required
def profile(request):
    if request.user.is_authenticated:
        try:
            person = UserProfile.objects.get(user = request.user)
        except UserProfile.DoesNotExist:
            user = None
            return render(request, 'sih/profile.html')            
        return render(request, 'sih/profile.html', { 'person':person})
    else:
        return redirect("/")

def profile_edit(request):
    form = None
    request.session['username'] = request.user.username
    user = User.objects.filter(username=request.user.username)
    print(user)
    userProfile = UserProfile.objects.get(user=request.user)
    print(userProfile)

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

    GENERAL = 'GENERAL'
    OBC =  'OBC'
    SC = 'SC'
    ST = 'ST'

    CATEGORY = (
        (GENERAL, GENERAL),
        (OBC,  OBC),
        (SC, SC),
        (ST, ST),
    )

    if request.user.is_authenticated:
        if request.method=="POST":
            form = UserProfileForm(request.POST)
            if form.is_valid():
                print (1)
                age = form.cleaned_data['age']
                gender = request.POST.get('gender')
                category = request.POST.get('category')
                qualification = request.POST.get('qualification')
                resume = request.FILES['resume']
                profilepicture = request.FILES['profilepicture']
                fs = FileSystemStorage()
                filename_resume = fs.save(resume.name, resume)
                uploaded_resume_url = fs.url(filename_resume)

                filename_profilepicture = fs.save(profilepicture.name, profilepicture)
                uploaded_profilepicture_url = fs.url(filename_profilepicture)
                is_subscribed = False
                if request.POST.get('is_subscribed')=="True":
                    is_subscribed = True
                user = User.objects.get(username=request.user.username)

                Profile = UserProfile.objects.create(user=user,age=age,gender=gender,category=category,resume=resume,profilepicture=profilepicture,is_subscribed=is_subscribed,qualification=qualification)
                Profile.save()

                return render(request, 'sih/complete_profile.html', {
                    'uploaded_resume_url': uploaded_resume_url,
                    'uploaded_profilepicture_url': uploaded_profilepicture_url,
                    'qualifications_choices':QUALIFICATIONS,
                    'gender_choices':GENDER,
                    'category_choices':CATEGORY
                })

        else:
            form = UserProfileForm()

        return render(request, 'sih/complete_profile.html', {'form': form, 'status':'logged_in','qualifications_choices':QUALIFICATIONS,'gender_choices':GENDER,'category_choices':CATEGORY})

    else:
        return redirect('sih:signup')

def vacancies(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = Vacancy(request.POST)
            if form.is_valid():
                title = request.POST.get('title')
                description = request.POST.get('description')
                num_slots = int(request.POST.get('num_slots'))
                location = request.POST.get('location')
                
                start_date = request.POST.get('start_date')

                end_date = request.POST.get('end_date')
                if request.POST.get('results_out')=="True":
                    results_out = True
                else:
                    results_out = False
                dept_user = DeptProfile.objects.get(user=request.user)
                New_vacancy = vacancy.objects.create(title=title,description=description,num_slots=num_slots,location=location,start_date=start_date,end_date=end_date,results_out=results_out,dept_id=dept_user)
                New_vacancy.save()
        else:
            form = Vacancy()
            
        return render(request, 'sih/vacancies.html', {'form': form, 'status':'logged_in'})

    else:
        return redirect('sih:signup')

def vacancy_detail(request):
    refer = request.META.get('HTTP_REFERER')
    vacancy = get_object_or_404(vacancy, pk=pk)
    if vacancy.end_date < timezone.now():
        messages.warning(request, 'This vacancy is expired')
        return redirect('/')
    else:
        return render(request, 'sih/vacancy_detail.html', {'vacancy': vacancy, 'refer': refer})
    return render(request, 'sih/vacancy_detail.html', {'vacancy': vacancy, 'refer': refer})

def query(request):
    if request.user.is_authenticated:
        pass

    else:
        return redirect('sih:signup')

def applications(request):
    if request.user.is_authenticated:
        pass

    else:
        return redirect('sih:signup')



