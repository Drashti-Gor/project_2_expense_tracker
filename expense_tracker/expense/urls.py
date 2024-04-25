from . import views
from django.contrib import admin
from django.urls import path

app_name = "expense"

urlpatterns = [     
    path("",views.home,name="home"),
    path("index/",views.index,name="index"),
    path("edit/<int:id>/",views.edit,name="edit"),
    path("delete/<int:id>/",views.delete,name="delete"),
    path("list_expenses/",views.list_expenses,name="list_expenses"),
    path("charts/",views.charts,name="charts"),
]