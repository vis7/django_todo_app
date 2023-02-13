import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import User

from .constants import CHANGE_STATUS, USER_PERMISSION


class ToDo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=32)
    due_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " - " + self.owner.username
    
class Change(models.Model):
    # ToDo Fields
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=32)
    due_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)

    # Other
    original_ref = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    change_status = models.CharField(choices=CHANGE_STATUS, max_length=32, default='created')
    change_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.change_by.username + ' - ' + self.change_status
    
class SharePermission(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(choices=USER_PERMISSION, max_length=32)

    def __str__(self):
        return self.todo.title + ' - ' + self.user.username + ' - ' + self.permission
    
class Log(models.Model):
    todo_id = models.IntegerField()
    updated_by = models.CharField(max_length=255) # username
    update_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id) + ' - ' + self.updated_by + ' - ' + str(self.update_time)
    