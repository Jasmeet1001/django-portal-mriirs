from django.urls import path
from . import views
from .views import UpdatePaperView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='dashboard-home'),
    # path('inj/', views.inj_view, name='dashboard-inj'),
    # path('inc/', views.inc_view, name='dashboard-inc'),
    # path('bkch/', views.book_chapter_view, name='dashboard-bkch'),
    path('paper/new/', views.add_new, name='dashboard-addpaper'),
    path('paper/<int:pk>/edit/', UpdatePaperView.as_view(), name='dashboard-edit'),
    path('paper/export', views.export_data, name='dashboard-export'),
    path('<str:username>/', views.profile_view, name='dashboard-profile'),
    path('<str:username>/paper/', views.my_papers, name='dashboard-mypaper'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)