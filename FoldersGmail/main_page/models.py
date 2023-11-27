from django.db import models

# Create your models here.
class Users(models.Model):
    login = models.CharField(max_length=300)
    password = models.CharField(max_length=300)

    def __str__(self):
        return self.login

class Folder(models.Model):
    title = models.CharField(max_length=300)
    discription = models.CharField()
    users = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Words(models.Model):
    words = models.CharField(max_length=100)
    foldres = models.ForeignKey(Folder, on_delete=models.CASCADE)

    def __str__(self):
        return self.words