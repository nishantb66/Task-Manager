# tasks/urls.py
from django.urls import path
from .views import (
    dashboard,
    create_task,
    edit_task,
    delete_task,
    toggle_pin,
    share_task,
    shared_tasks,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("share/", share_task, name="share_task"),
    path("shared/", shared_tasks, name="shared_tasks"),
    path("new/", create_task, name="create_task"),
    path("<int:pk>/toggle_pin/", toggle_pin, name="toggle_pin"),
    path("<int:pk>/edit/", edit_task, name="edit_task"),
    path("<int:pk>/delete/", delete_task, name="delete_task"),
]
