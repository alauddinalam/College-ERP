# accounts/urls.py
from django.urls import path
from . import views

app_name = 'myERP'

urlpatterns = [
    path('', views.signin, name='signin'),           # default route -> login page
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='signout'),
    # path('myerp/dashboard/', views.dashboard, name='dashboard'),
]
