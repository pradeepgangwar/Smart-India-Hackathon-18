from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):

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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_cofirmed = models.BooleanField(default=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=10, choices=GENDER)
    resume = models.FileField(blank=True, null =True)
    profilepicture = models.FileField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_subscribed = models.BooleanField(default=False)
    qualification = models.CharField(max_length=30, choices=QUALIFICATIONS)

class DeptProfile(models.Model):

    SuperUser = 'SuperUser'
    DeptAdmin =  'DeptAdmin'

    ROLES = (
        (SuperUser, SuperUser),
        (DeptAdmin,  DeptAdmin),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dept_name = models.CharField(max_length=300, null=False)
    role = models.CharField(max_length=30, choices=ROLES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class vacancy(models.Model):
    title = models.CharField(max_length=300,null=False)
    description = models.TextField(null=False)
    dept_id = models.ForeignKey(DeptProfile, on_delete=models.CASCADE)
    num_applicants = models.IntegerField(default=0, null=False)
    num_slots = models.IntegerField(default=0, null=False)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    updated_on = models.DateTimeField(auto_now = True)
    results_out = models.BooleanField(default=False)

class applications(models.Model):
    Pending = 'Pending'
    Rejected =  'Rejected'
    Accepted = 'Accepted'
    
    STATUS = (
        (Pending, Pending),
        (Rejected,  Rejected),
        (Accepted, Accepted),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dept = models.ForeignKey(vacancy,on_delete=models.CASCADE)
    application_status = models.CharField(max_length=30, choices=STATUS)
    sop = models.TextField(null=False)

class query(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dept = models.ForeignKey(vacancy,on_delete=models.CASCADE)
    question = models.CharField(max_length=300, null=False)
    answer = models.TextField(null=True)
    is_read = models.BooleanField(default=False)

class notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dept = models.ForeignKey(vacancy,on_delete=models.CASCADE)
    message = models.CharField(max_length=300, null=False)
    is_read = models.BooleanField(default=False)


