from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    date = models.DateField()
    approx_time = models.TimeField()
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class SharedTask(models.Model):
    sharer = models.ForeignKey(
        User, related_name="shared_out", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User, related_name="shared_in", on_delete=models.CASCADE
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sharer", "recipient", "task")
        ordering = ["-shared_at"]

    def __str__(self):
        return f"{self.task.title} shared from {self.sharer.username} to {self.recipient.username}"
