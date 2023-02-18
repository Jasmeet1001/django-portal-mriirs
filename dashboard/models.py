from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from PIL import Image

import datetime

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(default='default.jpg', upload_to='profile_pics')
    designation = models.CharField(max_length=20, blank=True)
    scopus_id = models.CharField(max_length=50, blank=True)
    wos_id = models.CharField(max_length=50, blank=True)
    citation_count = models.CharField(max_length=50, blank=True)
    month_year = models.CharField(max_length=50, blank=True)
    dept = models.CharField(max_length=7, blank=True)
    orcid_id = models.CharField(max_length=50, blank=True)
    vidwan_id = models.CharField(max_length=50, blank=True)
    h_index = models.CharField(max_length=10, blank=True)
    i_index = models.CharField(max_length=10, blank=True)
    is_new = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.pfp.path)

        if img.height > 300 or img.width > 300:
            resize_val = (300, 300)
            img.thumbnail(resize_val)
            img.save(self.pfp.path)

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class ResearchPaper(models.Model):
    users_associated = models.ManyToManyField(User)
    faculty = models.CharField(max_length=5, blank=True)
    authors = models.CharField(max_length=200, null=False, blank=False)
    outside_authors = models.CharField(max_length=200, blank=True)
    domain = models.CharField(max_length=255, blank=True)
    title_of_paper = models.CharField(max_length=255, blank=True)
    dept = models.CharField(max_length=50, blank=True)
    name_of_journal = models.CharField(max_length=255, blank=True)
    name_of_conference = models.CharField(max_length=255, blank=True)
    title_of_book = models.CharField(max_length=255, blank=True)
    title_of_chapter = models.CharField(max_length=255, blank=True)
    student = models.CharField(max_length=3, blank=True)
    scholar = models.CharField(max_length=3, blank=True)
    month = models.CharField(max_length=15, blank=True)
    year = models.CharField(max_length=15, blank=True)
    doi = models.URLField(blank=True)
    index_db = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f'{self.authors},{self.outside_authors}: {self.title_of_paper} {self.month}/{self.year}'
        # return f'{self.authors}: {self.title_of_paper} {self.month}/{self.year}'

    
    def get_absolute_url(self):
        return reverse('dashboard-edit', kwargs={'pk': self.pk})