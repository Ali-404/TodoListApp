from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TodoList(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    created_at = models.DateField()
    
    def __str__(self):
        return self.title


class Task(models.Model):
    todoList = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    complete = models.BooleanField()
    created_at = models.DateField()
    
    def __str__(self):
        return self.content
    
