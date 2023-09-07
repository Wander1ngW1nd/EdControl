from django.db import models


class Users(models.Model):
    email = models.TextField()
    login = models.TextField()
    password = models.TextField()
    salt = models.TextField()
    access_token = models.TextField()
    join_date = models.DateField()
    last_seen = models.DateTimeField()
    user_status = models.TextField()
    access_level = models.IntegerField()


    def __str__(self):
        return self.id


class UserInfo(models.Model):
    name = models.TextField()
    surname = models.TextField()
    organization = models.TextField()
    about = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


    def __str__(self):
        return self.id
