from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('internships/', views.internship_list, name='internship_list'),
    path('internships/<int:internship_id>/', views.internship_detail, name='internship_detail'),
    path('internships/<int:internship_id>/apply/', views.apply, name='apply'),
]
