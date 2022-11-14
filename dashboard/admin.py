from django.contrib import admin
from .models import Profile, ResearchPaper, AdditionalInfo

# Register your models here.
admin.site.register(Profile)
admin.site.register(ResearchPaper)
admin.site.register(AdditionalInfo)