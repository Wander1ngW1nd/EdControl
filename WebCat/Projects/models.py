from django.db import models
from Login.models import Users


class Project(models.Model):
    name = models.TextField()
    about = models.TextField()
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
