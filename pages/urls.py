# pages/urls.py
from django.urls import path
from .views import homePageView, aboutPageView, results, homePost

urlpatterns = [
    path('', homePageView, name='home'),
    path('about/', aboutPageView, name='about'),
    path('homePost/', homePost, name='homePost'),
    path('results/<int:age>/<str:gender>/<int:appearance_score>/<str:job_type>/<str:educational_status>/', results, name='results'),

]
