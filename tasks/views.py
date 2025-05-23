# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Task
from .models import SharedTask
from .forms import TaskForm
from django.contrib import messages

User = get_user_model()


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user).order_by(
        "-pinned", "-date", "-approx_time"
    )
    all_users = User.objects.all()  # for the share-modal datalist
    return render(
        request,
        "tasks/dashboard.html",
        {"tasks": tasks, "all_users": all_users},
    )


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


@login_required
def toggle_pin(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.pinned = not task.pinned
    task.save()
    return redirect("dashboard")


@login_required
def share_task(request):
    """
    POST only: expects 'recipient_username' and 'task_id' in request.POST.
    """
    if request.method == "POST":
        recipient_username = request.POST.get("recipient_username", "").strip()
        task_id = request.POST.get("task_id")
        # find recipient
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            messages.error(request, "That user does not exist.")
            return redirect("dashboard")

        # find and validate task belongs to sharer
        task = get_object_or_404(Task, pk=task_id, user=request.user)

        # create share
        SharedTask.objects.get_or_create(
            sharer=request.user, recipient=recipient, task=task
        )
        messages.success(request, f"“{task.title}” shared with {recipient.username}.")
    return redirect("dashboard")


@login_required
def shared_tasks(request):
    """
    Show all tasks shared *to* this user.
    """
    shared_list = SharedTask.objects.filter(recipient=request.user).select_related(
        "task__user", "sharer"
    )
    return render(request, "tasks/shared_tasks.html", {"shared_list": shared_list})
