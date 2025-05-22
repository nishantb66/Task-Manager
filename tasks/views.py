# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user).order_by("-date", "-approx_time")
    return render(request, "tasks/dashboard.html", {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            return redirect("dashboard")
    else:
        form = TaskForm()
    return render(request, "tasks/create_task.html", {"form": form})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/edit_task.html", {"form": form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("dashboard")
    # GET → confirmation page
    return render(request, "tasks/confirm_delete.html", {"task": task})
