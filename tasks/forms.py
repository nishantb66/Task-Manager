# tasks/forms.py
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "date", "approx_time", "email", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": (
                        "w-full px-3 py-2 "
                        "bg-white bg-opacity-90 text-black "
                        "border border-white/20 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-white/50"
                    ),
                    "placeholder": "Task title",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": (
                        "w-full px-3 py-2 "
                        "bg-white bg-opacity-90 text-black "
                        "border border-white/20 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-white/50"
                    ),
                }
            ),
            "approx_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": (
                        "w-full px-3 py-2 "
                        "bg-white bg-opacity-90 text-black "
                        "border border-white/20 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-white/50"
                    ),
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": (
                        "w-full px-3 py-2 "
                        "bg-white bg-opacity-90 text-black "
                        "border border-white/20 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-white/50"
                    ),
                    "placeholder": "Optional email",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": (
                        "w-full px-3 py-2 "
                        "bg-white bg-opacity-90 text-black "
                        "border border-white/20 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-white/50"
                    ),
                    "placeholder": "Optional description",
                }
            ),
        }
