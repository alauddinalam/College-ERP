from django.urls import path
from . import views

app_name = 'myERP'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('attendance/', views.attendance, name="attendance"),
    path('fee/', views.fee, name="fee"),
    path('profile/', views.profile, name="profile"),
    path('subjects/', views.subjects, name="subjects"),
    path('notices/', views.notices, name="notices"),
]
