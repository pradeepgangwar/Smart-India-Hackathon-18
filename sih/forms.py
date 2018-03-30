from django import forms
from .models import *

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
    
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('age', 'gender', 'resume', 'profilepicture', 'qualification')

class DeptProfile(forms.ModelForm):

    class Meta:
        model = DeptProfile
        fields = ('dept_name', 'role')

class Vacancy(forms.ModelForm):

    class Meta:
        model = vacancy
        fields = ('title', 'description', 'num_slots', 'start_date', 'end_date', 'results_out')

class Applications(forms.ModelForm):

    class Meta:
        model = applications
        fields = ('sop')

class Query(forms.ModelForm):

    class Meta:
        model = query
        fields = ('question')
       