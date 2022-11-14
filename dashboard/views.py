from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import ResearchPaper
from .forms import UserUpdateForm, ProfileUpdateForm, AddPaper, ImportFile, AdditionalInfoUpdateForm

from .import_paper import import_excel

# Create your views here.
class UpdatePaperView(LoginRequiredMixin, UpdateView):
    model = ResearchPaper
    fields = ['authors', 'affilation', 'domain', 'doi', 'month', 'year']
    template_name = 'dashboard/paper_edit.html'

@login_required
def homepage(request):
    search = ''
    if request.GET.get('search-result'):
        search = request.GET.get('search-result')

    paper_list = ResearchPaper.objects.filter(
        Q(authors__icontains=search) | 
        Q(domain__icontains=search) | 
        Q(affilation__icontains=search) | 
        Q(month__icontains=search) | 
        Q(year__icontains=search)).order_by('-id')
    # paper_all = ResearchPaper.objects.all().order_by('-id')
    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'paper_list': paper_list,
        'paper_count': paper_list.count(),
        'page_obj': page_obj,
        'search': str(search)
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
                if (request.FILES['fileupload-file'].name[-4:] == 'xlsx' or request.FILES['fileupload-file'].name[-3:] == 'xls'):
                    message = import_excel(request.FILES['fileupload-file'])
                    if 'Successful' in message:
                        messages.success(request, f"{message}")
                    else:
                        messages.error(request, f"{message}")
                else:
                    messages.error(request, "Invalid file type! Only xlsx or xls formats are supported.")
            
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
            messages.success(request, 'Updated profile information')
            return redirect('dashboard-profile')
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