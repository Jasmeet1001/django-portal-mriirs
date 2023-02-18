from django import forms
from django.contrib.auth.models import User
from .models import Profile, ResearchPaper
# , AdditionalInfo, current_year

import datetime

class Signup(forms.Form):
    choices = (
        ('1', 'Admin'),
        ('2', 'Faculty')
    )
    choice = forms.ChoiceField(choices=choices, label='Create Account For: ')
    email = forms.EmailField(required=True)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['designation', 'scopus_id', 'wos_id', 'citation_count', 'month_year', 'dept', 'orcid_id', 'vidwan_id', 'h_index', 'i_index', 'pfp']
        labels = {'pfp': 'Profile Image', 'dept': 'Department'}

def year_choices():
    return [(year, year) for year in range(2000, datetime.date.today().year+1)]

class AddPaper(forms.ModelForm):
    # year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, required=False)
    class Meta:
        model = ResearchPaper
        fields = ['faculty', 'authors', 'outside_authors', 'domain', 'title_of_paper', 'dept', 'name_of_journal', 'name_of_conference', 'title_of_book', 'title_of_chapter', 'student', 'scholar', 'month', 'year', 'doi', 'index_db']
        
        labels = {'dept': 'Department', 'index_db': 'Index databse (SCOPUS, SCIE, ESCI, UGC CARE)', 'faculty': 'Faculty (Ex: FET)', 'authors': 'Authors Name', 'domain': 'Domain (Ex: Machine Learning, NLP, etc)', 'student': 'Student (y/n)', 'scholar': 'Scholar (y/n)', 'year': 'Publication Year','month': 'Publication Month'}
    
class ImportFile(forms.Form):
    file = forms.FileField(label='')