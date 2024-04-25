from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns=[
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout1,name='logout'),
    
]