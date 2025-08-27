from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/quests/", views.quests_list, name="quests_list"),
]
