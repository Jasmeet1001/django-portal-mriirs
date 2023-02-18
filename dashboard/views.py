from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
# from django.core.files.storage import FileSystemStorage as fs

from .models import ResearchPaper
from .forms import UserUpdateForm, ProfileUpdateForm, AddPaper, ImportFile, Signup
# , AdditionalInfoUpdateForm

from .imp_exp import import_excel, pd

import uuid

# Create your views here.
SEARCH_UN = ''

def is_admin(user):
    return user.groups.filter(name="adminstaff").exists()

class UpdatePaperView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ResearchPaper
    fields = [ 'faculty', 'outside_authors', 'domain', 'title_of_paper', 'dept', 'name_of_journal', 'name_of_conference', 'title_of_book', 'title_of_chapter', 'student', 'scholar', 'month', 'year', 'doi', 'index_db']

    def test_func(self):
        paper = self.get_object()
        if self.request.user in paper.users_associated.all() or is_admin(self.request.user): #type:ignore
            return True
        return False

    template_name = 'dashboard/paper_edit.html'

@login_required
@user_passes_test(is_admin, login_url='/forbidden/', redirect_field_name=None) #type:ignore
def del_user_view(request, pk):
    user_to_del = User.objects.get(pk=pk)
    if request.method == 'POST':
        user_to_del.delete()
        return redirect(reverse('create-account'))

    context = {
        'object': user_to_del.username
    }

    return render(request, 'dashboard/user_delete.html', context)

def search():
    global SEARCH_UN
    terms = SEARCH_UN.strip().split(';')
    paper_list = []
    try:
        if len(terms) == 1 and ':' not in terms[0]:
        # if len(SEARCH) == 1:
            paper_list = ResearchPaper.objects.filter(
                Q(faculty__icontains=terms[0]) | 
                Q(authors__icontains=terms[0]) | 
                Q(outside_authors__icontains=terms[0]) | 
                Q(title_of_paper__icontains=terms[0]) | 
                Q(dept__icontains=terms[0]) | 
                Q(name_of_journal__icontains=terms[0]) | 
                Q(name_of_conference__icontains=terms[0]) | 
                Q(title_of_book__icontains=terms[0]) |
                Q(title_of_chapter__icontains=terms[0]) |
                Q(scholar__icontains=terms[0]) | 
                Q(month__icontains=terms[0]) |
                Q(year__icontains=terms[0]) |
                Q(index_db__icontains=terms[0])).order_by('-id')

        elif len(terms) >= 1:
            query = []
            for term in terms:
                #faculty:FET; department:CSE
                #['faculty:FET', 'department:CSE']
                #['faculty', 'FET']
                SEARCH = term.strip().split(':')
                to_scr = SEARCH[1].strip()
                match SEARCH[0].strip():
                    case 'faculty':
                        if query:
                            query = query.filter(faculty__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(faculty__icontains=to_scr).order_by('-id')
                    
                    case 'authors':
                        if query:
                            query = query.filter(authors__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(authors__icontains=to_scr).order_by('-id')
                    
                    case 'oauthors':
                        if query:
                            query = query.filter(authors__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(authors__icontains=to_scr).order_by('-id')

                    case 'domain':
                        if query:
                            query = query.filter(domain__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(domain__icontains=to_scr).order_by('-id')
    
                    case 'top':
                        if query:
                            query = query.filter(title_of_paper__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(title_of_paper__icontains=to_scr).order_by('-id')
                        
                    case 'department':
                        if query:
                            query = query.filter(dept__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(dept__icontains=to_scr).order_by('-id')
                        
                    case 'noj':
                        if query:
                            query = query.filter(name_of_journal__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(name_of_journal__icontains=to_scr).order_by('-id')
                        
                    case 'noc':
                        if query:
                            query = query.filter(name_of_conference__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(name_of_conference__icontains=to_scr).order_by('-id')
                        
                    case 'tob':
                        if query:
                            query = query.filter(title_of_book__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(title_of_book__icontains=to_scr).order_by('-id')
                        
                    case 'toc':
                        if query:
                            query = query.filter(title_of_chapter__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(title_of_chapter__icontains=to_scr).order_by('-id')
                        
                    case 'scholar':
                        if query:
                            query = query.filter(scholar__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(scholar__icontains=to_scr).order_by('-id')
                        
                    case 'student':
                        if query:
                            query = query.filter(student__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(student__icontains=to_scr).order_by('-id')
                        
                    case 'month':
                        if query:
                            query = query.filter(month__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(month__icontains=to_scr).order_by('-id')
                        
                    case 'year':
                        # if '-' in to_scr:
                            # yr_range = to_scr.split('-')
                            # if query:
                                # query = query.filter(year__range=(yr_range[0], yr_range[1]).order_by('-id') # type: ignore
                            # else:
                                # query = ResearchPaper.objects.filter(year__range=(yr_range[0], yr_range[1]).order_by('-id')
                        # else:
                        if query:
                            query = query.filter(year__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(year__icontains=to_scr).order_by('-id')
                        
                    case 'idb':
                        if query:
                            query = query.filter(index_db__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(index_db__icontains=to_scr).order_by('-id')
            paper_list = query
    except:
        paper_list = []                   
    return paper_list

@login_required
def export_data(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={uuid.uuid4()}.xlsx'
    object = []
    if SEARCH_UN == '':
        object = ResearchPaper.objects.all()
    else:
        object = search()
    data = []
    for obj in object:
        data.append(
            {
                'faculty': obj.faculty,
                'authors': obj.authors,
                'outside authors': obj.outside_authors,
                'domain': obj.domain,
                'title of paper': obj.title_of_paper,
                'dept.': obj.dept,
                'name of journal': obj.name_of_journal,
                'name of conference': obj.name_of_conference,
                'title of book': obj.title_of_book,
                'title of chapter': obj.title_of_chapter,
                'student': obj.student,
                'scholar': obj.scholar,
                'publication month': obj.month,
                'publication year': obj.year,
                'doi': obj.doi,
                'index database': obj.index_db
            }
        )
    df = pd.DataFrame(data)
    df.to_excel(response, index=False)
    return response

@login_required
def template_download(request):
    filename = 'sample_template'
    data = { 'faculty': ['FET'], 'authors': ['author1,author1'], 'outside authors': ['outside author1, outside author1(optional)'], 'domain':['Machine Learning'], 'title of paper': ['title'], 'dept.': ['Mechanical Engineering'], 'name of journal': ['journal name'], 'name of conference': ['conference name'], 'title of book': ['name of book'], 'title of chapter': ['name of chapter'], 'student':['y/n or yes/no'], 'scholar':['y/n or yes/no'], 'publication month': ['March'], 'publication year':['start year-end year(2020-2020, 2020-2021)'], 'doi':['doi link'], 'index database': ['(SCOPUS, SCIE, ESCI, UGC CARE)']}

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
    df = pd.DataFrame(data=data)
    df.to_excel(response, index=False)
    return response

def is_new(user):
    if user.profile.is_new:
        user.profile.is_new = False
        user.save()
        return True
    else:
        return False

@login_required
# @user_passes_test(is_new, login_url='/password-change/')
def homepage(request):
    if request.user.profile.is_new:
        request.user.profile.is_new = False
        request.user.save()
        return redirect('password_change')

    global SEARCH_UN
    SEARCH_UN = ''
    if request.GET.get('search-result'):
        SEARCH_UN = request.GET.get('search-result')
    
    paper_list = search()

    # # paper_all = ResearchPaper.objects.all().order_by('-id')
    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'paper_list': paper_list,
        'paper_count': len(paper_list),
        'page_obj': page_obj,
        'search': str(SEARCH_UN),
        'is_admin': is_admin(request.user),
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def inj_view(request):
    #Need name of journal column
    # if SEARCH_UN != '':
    #     paper_list = search()
    # else:
    paper_list = ResearchPaper.objects.exclude(name_of_journal__iexact='').order_by('-id')

    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paper_count': len(paper_list),
        'page_obj': page_obj,
        'search': str(SEARCH_UN),
        'is_admin': is_admin(request.user)
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def inc_view(request):
    #Need name of conference
    # if SEARCH_UN != '':
    #     paper_list = search()
    # else:
    paper_list = ResearchPaper.objects.exclude(name_of_conference__iexact='').order_by('-id')

    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paper_count': len(paper_list),
        'page_obj': page_obj,
        'search': str(SEARCH_UN),
        'is_admin': is_admin(request.user)
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def book_chapter_view(request):
    #Need name of book and name of chapter
    # if SEARCH_UN != '':
    #     paper_list = search()
    # else:
    paper_list = ResearchPaper.objects.exclude(title_of_book__iexact='', title_of_chapter__iexact='').order_by('-id')

    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paper_count': len(paper_list),
        'page_obj': page_obj,
        'search': str(SEARCH_UN),
        'is_admin': is_admin(request.user)
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def my_papers(request, username):
    if username == request.user.username:
        paper_affiliated = ResearchPaper.objects.filter(users_associated__username=username).order_by('-id')
        paper_count = paper_affiliated.count()
        can_edit = True
        paginator = Paginator(paper_affiliated, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context={
                'paper_count': paper_count,
                'page_obj': page_obj,
                'can_edit': can_edit,
                'is_admin': is_admin(request.user)
            }    
        return render(request, 'dashboard/home.html', context)
    else:
        return redirect('login')


@login_required
def add_new(request):
    if request.method == 'POST':
        fileupload_form = ImportFile(prefix='fileupload')
        addpaper_form = AddPaper(prefix='singleupload')
        if 'import' in request.POST:
            fileupload_form = ImportFile(request.POST, request.FILES, prefix='fileupload')
            valid_formats = ['xlsx', 'xls', 'csv']
            if fileupload_form.is_valid():
                if (request.FILES['fileupload-file'].name.split('.')[-1] in valid_formats):
                    message = import_excel(request, request.FILES['fileupload-file'])
                    if 'Successful' in message[0]:
                        messages.success(request, f"{message[0]}")
                    else:
                        messages.error(request, f"{message[0]}")
                    message[1].delete(request.FILES['fileupload-file'].name)
                else:
                    messages.error(request, "Invalid file type! Only xlsx, xls or csv formats are supported.")
            
        elif 'add-details' in request.POST:
            addpaper_form = AddPaper(request.POST, prefix='singleupload')
            if addpaper_form.is_valid():
                clean_form = addpaper_form.cleaned_data
                if (ResearchPaper.objects.filter(title_of_paper__iexact = clean_form.get('title_of_paper')).exists()):
                    # Update the already existing row with new user
                    curr_paper = ResearchPaper.objects.get(title_of_paper = clean_form.get('title_of_paper'))
                    curr_paper.authors = curr_paper.authors + f",{clean_form.get('authors')}"
                    curr_paper.authors = curr_paper.authors.rstrip(', ')
                    curr_paper.outside_authors = curr_paper.outside_authors + f" {clean_form.get('outside_authors')}"
                    curr_paper.outside_authors = curr_paper.outside_authors.rstrip(', ')
                    curr_paper.save()
                    curr_user = User.objects.get(pk=request.user.pk)
                    curr_paper.users_associated.add(curr_user)
                    # curr_paper.users_associated.set([curr_user])
                    # -------------------------------------------
                    # curr_paper.users_associated.add(request.user)
                    # curr_paper.users_associated.set([request.user])
                else:
                    addpaper_form.save()
                    curr_paper = ResearchPaper.objects.get(title_of_paper = clean_form.get('title_of_paper'))
                    curr_user = User.objects.get(pk=request.user.pk)
                    curr_paper.users_associated.add(curr_user)
                    # user_add = clean_form.get('users_associated')
                    # user_add = curr_user

                messages.success(request, 'Added Details Successfully')
                return redirect('dashboard-addpaper')

    else:
        fileupload_form = ImportFile(prefix='fileupload')
        addpaper_form = AddPaper(prefix='singleupload')

    context = {
        'fileupload_form': fileupload_form,
        'addpaper_form': addpaper_form,
        'is_admin': is_admin(request.user)
    }

    return render(request, 'dashboard/add_paper.html', context)

@login_required
@user_passes_test(is_admin, login_url = '/forbidden/', redirect_field_name=None) #type:ignore
def create_account(request):
    faculty_accounts = User.objects.filter(groups__name='faculty')
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = User.objects.make_random_password(length=8, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            usrname = email.split('@')[0].split('.')[0]
            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with that email already exists")
            else:
                user_type = form.cleaned_data.get('choice')
                group = Group()
                if user_type == '1':
                    group = Group.objects.get(name="adminstaff")
                elif user_type == '2':
                    group = Group.objects.get(name="faculty")
                User.objects.create_user(usrname, email, password)
                User.objects.get(username=usrname).groups.add(group)
                messages.success(request, f"Account created for {email} with password {password}")
                return redirect('create-account')
    else:
        form = Signup()
    context = {
        'form': form,
        'f_acc': faculty_accounts,
    }

    return render(request, 'dashboard/add_account.html', context)

@login_required
@user_passes_test(is_admin, login_url='/forbidden/', redirect_field_name=None) #type:ignore
def show_facpaper_view(request, pk):
    paper_to_get = ResearchPaper.objects.filter(users_associated__pk=pk)

    paginator = Paginator(paper_to_get, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paper_count': len(paper_to_get),
        'page_obj': page_obj,
        'search': str(SEARCH_UN),
        'is_admin': is_admin(request.user)
    }
    return render(request, 'dashboard/home.html', context)



@login_required
def profile_view(request, username):
    if username == request.user.username:
        if request.method == 'POST':
            user_update = UserUpdateForm(request.POST, instance=request.user)
            profile_update = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

            if user_update.is_valid() and profile_update.is_valid():
                user_update.save()
                profile_update.save()
                messages.success(request, 'Updated profile information')
                return redirect('dashboard-profile', username=request.user.username)
        else:
            user_update = UserUpdateForm(instance=request.user)
            profile_update = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_update': user_update,
            'profile_update': profile_update,
            'is_admin': is_admin(request.user)
        }
        return render(request, 'dashboard/profile.html', context)
    else:
        return redirect('login')

# @user_passes_test()
# def set_password(self):
#     pass