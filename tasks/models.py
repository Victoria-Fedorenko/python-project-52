from django.db import models
from django.contrib.auth import get_user_model
from statuses.models import Status  

User = get_user_model()

class Task(models.Model):

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,          # запрет удаления статуса, если есть задачи
        related_name='tasks'              # чтобы использовать status.tasks.exists()
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_tasks'
    )   
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executed_tasks',
        null=True,
        blank=True
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

