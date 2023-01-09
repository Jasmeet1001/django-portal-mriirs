from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import ResearchPaper
from .forms import UserUpdateForm, ProfileUpdateForm, AddPaper, ImportFile, AdditionalInfoUpdateForm

from .imp_exp import import_excel, pd

# Create your views here.
SEARCH_UN = ''

class UpdatePaperView(LoginRequiredMixin, UpdateView):
    model = ResearchPaper
    fields = [ 'faculty', 'authors', 'domain', 'title_of_paper', 'dept', 'name_of_journal', 'name_of_conference', 'title_of_book', 'title_of_chapter', 'student', 'scholar', 'month', 'year', 'doi', 'index_db']
    template_name = 'dashboard/paper_edit.html'

def search():
    SEARCH = SEARCH_UN.strip().split(':')
    paper_list = []
    if len(SEARCH) == 1:
        paper_list = ResearchPaper.objects.filter(
            Q(faculty__icontains=SEARCH[0]) | 
            Q(authors__icontains=SEARCH[0]) | 
            Q(title_of_paper__icontains=SEARCH[0]) | 
            Q(dept__icontains=SEARCH[0]) | 
            Q(name_of_journal__icontains=SEARCH[0]) | 
            Q(name_of_conference__icontains=SEARCH[0]) | 
            Q(title_of_book__icontains=SEARCH[0]) |
            Q(title_of_chapter__icontains=SEARCH[0]) |
            Q(scholar__icontains=SEARCH[0]) | 
            Q(month__icontains=SEARCH[0]) |
            Q(year__icontains=SEARCH[0]) |
            Q(index_db__icontains=SEARCH[0])).order_by('-id')

    elif len(SEARCH) == 2:
        to_scr = SEARCH[1].strip()
        match SEARCH[0].strip():
            case 'faculty':
                paper_list = ResearchPaper.objects.filter(faculty__icontains=to_scr).order_by('-id')
            case 'authors':
                paper_list = ResearchPaper.objects.filter(authors__icontains=to_scr).order_by('-id')
            case 'domain':
                paper_list = ResearchPaper.objects.filter(domain__icontains=to_scr).order_by('-id')
            case 'title of paper':
                paper_list = ResearchPaper.objects.filter(title_of_paper__icontains=to_scr).order_by('-id')
            case 'department':
                paper_list = ResearchPaper.objects.filter(dept__icontains=to_scr).order_by('-id')
            case 'name of journal':
                paper_list = ResearchPaper.objects.filter(name_of_journal__icontains=to_scr).order_by('-id')
            case 'name of conference':
                paper_list = ResearchPaper.objects.filter(name_of_conference__icontains=to_scr).order_by('-id')
            case 'title of book':
                paper_list = ResearchPaper.objects.filter(title_of_book__icontains=to_scr).order_by('-id')
            case 'title of chapter':
                paper_list = ResearchPaper.objects.filter(title_of_chapter__icontains=to_scr).order_by('-id')
            case 'scholar':
                paper_list = ResearchPaper.objects.filter(scholar__icontains=to_scr).order_by('-id')
            case 'student':
                paper_list = ResearchPaper.objects.filter(student__icontains=to_scr).order_by('-id')
            case 'month':
                paper_list = ResearchPaper.objects.filter(month__icontains=to_scr).order_by('-id')
            case 'year':
                paper_list = ResearchPaper.objects.filter(year__icontains=to_scr).order_by('-id')
            case 'scopus id':
                paper_list = ResearchPaper.objects.filter(index_db__icontains=to_scr).order_by('-id')
    
    return paper_list

@login_required
def export_data(request):
    import uuid
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={uuid.uuid4()}.xlsx'
    object = []
    # SEARCH = SEARCH_UN.strip().split(':')
    if SEARCH_UN == '':
        object = ResearchPaper.objects.all()
    else:
        object = search()
        # if len(SEARCH) == 1:
        #     object = ResearchPaper.objects.filter(
        #         Q(faculty__icontains=SEARCH[0]) | 
        #         Q(authors__icontains=SEARCH[0]) | 
        #         Q(title_of_paper__icontains=SEARCH[0]) | 
        #         Q(dept__icontains=SEARCH[0]) | 
        #         Q(name_of_journal__icontains=SEARCH[0]) | 
        #         Q(name_of_conference__icontains=SEARCH[0]) | 
        #         Q(title_of_book__icontains=SEARCH[0]) |
        #         Q(title_of_chapter__icontains=SEARCH[0]) |
        #         Q(scholar__icontains=SEARCH[0]) | 
        #         Q(student__icontains=SEARCH[0]) |
        #         Q(month__icontains=SEARCH[0]) |
        #         Q(year__icontains=SEARCH[0]) |
        #         Q(index_db__icontains=SEARCH[0])).order_by('-id') 
        # elif len(SEARCH) == 2:
        #     to_search = SEARCH[1].strip()
        #     match SEARCH[0].strip():
        #         case 'faculty':
        #             object = ResearchPaper.objects.filter(faculty__icontains=to_search).order_by('-id')
        #         case 'authors':
        #             object = ResearchPaper.objects.filter(authors__icontains=to_search).order_by('-id')
        #         case 'domain':
        #             object = ResearchPaper.objects.filter(domain__icontains=to_search).order_by('-id')
        #         case 'title of paper':
        #             object = ResearchPaper.objects.filter(title_of_paper__icontains=to_search).order_by('-id')
        #         case 'department':
        #             object = ResearchPaper.objects.filter(dept__icontains=to_search).order_by('-id')
        #         case 'name of journal':
        #             object = ResearchPaper.objects.filter(name_of_journal__icontains=to_search).order_by('-id')
        #         case 'name of conference':
        #             object = ResearchPaper.objects.filter(name_of_conference__icontains=to_search).order_by('-id')
        #         case 'title of book':
        #             object = ResearchPaper.objects.filter(title_of_book__icontains=to_search).order_by('-id')
        #         case 'title of chapter':
        #             object = ResearchPaper.objects.filter(title_of_chapter__icontains=to_search).order_by('-id')
        #         case 'scholar':
        #             object = ResearchPaper.objects.filter(scholar__icontains=to_search).order_by('-id')
        #         case 'student':
        #             object = ResearchPaper.objects.filter(student__icontains=to_search).order_by('-id')
        #         case 'month':
        #             object = ResearchPaper.objects.filter(month__icontains=to_search).order_by('-id')
        #         case 'year':
        #             object = ResearchPaper.objects.filter(year__icontains=to_search).order_by('-id')
        #         case 'scopus id':
        #             object = ResearchPaper.objects.filter(index_db__icontains=to_search).order_by('-id')

    data = []

    for obj in object:
        data.append(
            {
                'faculty': obj.faculty,
                'authors': obj.authors,
                'domain': obj.domain,
                'title of paper': obj.title_of_paper,
                'dept.': obj.dept,
                'name of journal': obj.name_of_journal,
                'name of conference': obj.name_of_conference,
                'title of book': obj.title_of_book,
                'title of chapter': obj.title_of_chapter,
                'student': obj.student,
                'scholar': obj.scholar,
                'month': obj.month,
                'year': obj.year,
                'doi': obj.doi,
                'index database': obj.index_db
            }
        )
    df = pd.DataFrame(data)
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
    if SEARCH_UN != '':
        paper_list = search()
    else:
        paper_list = ResearchPaper.objects.filter(name_of_journal__exact='')

    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'paper_count': len(paper_list),
        'page_obj': page_obj,
        'search': str(SEARCH_UN)
    }
    return render(request, 'dashboard/inj.html', context)

def inc_view(request):
    #Need name 
    pass

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
        additional_info = AdditionalInfoUpdateForm(request.POST, instance=request.user.additionalinfo)
        user_update = UserUpdateForm(request.POST, instance=request.user)
        profile_update = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_update.is_valid() and profile_update.is_valid():
            user_update.save()
            profile_update.save()
            additional_info.save()
            messages.success(request, 'Updated profile information')
            return redirect('dashboard-profile', username=request.user.username)
    else:
        user_update = UserUpdateForm(instance=request.user)
        profile_update = ProfileUpdateForm(instance=request.user.profile)
        additional_info = AdditionalInfoUpdateForm(instance=request.user.additionalinfo)

    context = {
        'user_update': user_update,
        'profile_update': profile_update,
        'additional_info': additional_info,
    }
    return render(request, 'dashboard/profile.html', context)