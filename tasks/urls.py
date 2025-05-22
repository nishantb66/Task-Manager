# tasks/urls.py
from django.urls import path
from .views import dashboard, create_task, edit_task, delete_task

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("new/", create_task, name="create_task"),
    path("<int:pk>/edit/", edit_task, name="edit_task"),
    path("<int:pk>/delete/", delete_task, name="delete_task"),
]
