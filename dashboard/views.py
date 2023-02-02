from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import ResearchPaper
from .forms import UserUpdateForm, ProfileUpdateForm, AddPaper, ImportFile
# , AdditionalInfoUpdateForm

from .imp_exp import import_excel, pd

import uuid

# Create your views here.
SEARCH_UN = ''

class UpdatePaperView(LoginRequiredMixin, UpdateView):
    model = ResearchPaper
    fields = [ 'faculty', 'authors', 'domain', 'title_of_paper', 'dept', 'name_of_journal', 'name_of_conference', 'title_of_book', 'title_of_chapter', 'student', 'scholar', 'month', 'year', 'doi', 'index_db']
    template_name = 'dashboard/paper_edit.html'

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
                        
                    case 'domain':
                        if query:
                            query = query.filter(domain__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(domain__icontains=to_scr).order_by('-id')
    
                    case 'title of paper':
                        if query:
                            query = query.filter(title_of_paper__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(title_of_paper__icontains=to_scr).order_by('-id')
                        
                    case 'department':
                        if query:
                            query = query.filter(dept__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(dept__icontains=to_scr).order_by('-id')
                        
                    case 'name of journal':
                        if query:
                            query = query.filter(name_of_journal__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(name_of_journal__icontains=to_scr).order_by('-id')
                        
                    case 'name of conference':
                        if query:
                            query = query.filter(name_of_conference__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(name_of_conference__icontains=to_scr).order_by('-id')
                        
                    case 'title of book':
                        if query:
                            query = query.filter(title_of_book__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(title_of_book__icontains=to_scr).order_by('-id')
                        
                    case 'title of chapter':
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
                        if query:
                            query = query.filter(year__icontains=to_scr).order_by('-id') # type: ignore
                        else:
                            query = ResearchPaper.objects.filter(year__icontains=to_scr).order_by('-id')
                        
                    case 'index db':
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
                'outside author': '',
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
    col_include = [ 'faculty', 'authors', 'outside author', 'domain', 'title of paper', 'dept.', 'name of journal', 'name of conference', 'title of book', 'title of chapter', 'student', 'scholar', 'publication month', 'publication year', 'doi', 'index database']

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
    df = pd.DataFrame(columns=col_include)
    df.to_excel(response, index=False)
    return response

@login_required
def homepage(request):
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
        'search': str(SEARCH_UN)
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def inj_view(request):
    #Need name of journal column
    # if SEARCH_UN != '':
    #     paper_list = search()
    # else:
    paper_list = ResearchPaper.objects.exclude(name_of_journal__exact='').order_by('-id')

    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paper_count': len(paper_list),
        'page_obj': page_obj,
        'search': str(SEARCH_UN)
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def inc_view(request):
    #Need name of conference
    # if SEARCH_UN != '':
    #     paper_list = search()
    # else:
    paper_list = ResearchPaper.objects.exclude(name_of_conference__exact='').order_by('-id')

    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paper_count': len(paper_list),
        'page_obj': page_obj,
        'search': str(SEARCH_UN)
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def book_chapter_view(request):
    #Need name of book and name of chapter
    # if SEARCH_UN != '':
    #     paper_list = search()
    # else:
    paper_list = ResearchPaper.objects.exclude(Q(title_of_book__exact='') | Q(title_of_chapter__exact='')).order_by('-id')

    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paper_count': len(paper_list),
        'page_obj': page_obj,
        'search': str(SEARCH_UN)
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def my_papers(request, username):
    full_name = f'{request.user.first_name} {request.user.last_name}'
    paper_affiliated = ResearchPaper.objects.filter(authors__icontains=full_name.rstrip()).order_by('-id')
    paper_count = paper_affiliated.count()

    paginator = Paginator(paper_affiliated, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if full_name.rstrip() != '':
        context={
            'paper_count': paper_count,
            'page_obj': page_obj
        }
    else:
        context = {
            'paper_count': 0,
            'page_obj': ''
        }
    
    return render(request, 'dashboard/home.html', context)


@login_required
def add_new(request):
    if request.method == 'POST':
        fileupload_form = ImportFile(prefix='fileupload')
        addpaper_form = AddPaper(prefix='singleupload')
        if 'import' in request.POST:
            fileupload_form = ImportFile(request.POST, request.FILES, prefix='fileupload')
            if fileupload_form.is_valid():
                if (request.FILES['fileupload-file'].name[-4:] == 'xlsx' or request.FILES['fileupload-file'].name[-3:] == 'xls' or request.FILES['fileupload-file'].name[-3:] == 'csv'):
                    message = import_excel(request.FILES['fileupload-file'])
                    if 'Successful' in message:
                        messages.success(request, f"{message}")
                    else:
                        messages.error(request, f"{message}")
                else:
                    messages.error(request, "Invalid file type! Only xlsx, xls or csv formats are supported.")
            
        elif 'add-details' in request.POST:
            addpaper_form = AddPaper(request.POST, prefix='singleupload')
            if addpaper_form.is_valid():
                addpaper_form.save()
                messages.success(request, 'Added Details Successfully')
                return redirect('dashboard-addpaper')

    else:
        fileupload_form = ImportFile(prefix='fileupload')
        addpaper_form = AddPaper(prefix='singleupload')

    context = {
        'fileupload_form': fileupload_form,
        'addpaper_form': addpaper_form
    }

    return render(request, 'dashboard/add_paper.html', context)

@login_required
def profile_view(request, username):
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
    }
    return render(request, 'dashboard/profile.html', context)