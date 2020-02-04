from django.db import models
# Create your models here.

# this class will  define the Clients ( Arduino ) Model .
# Name : The name of this client . e.g : Lights .
# Number ID : The number of this client in this project . e.g : 8
# User : The project . e.g : Mohammad's project


class Client(models.Model):
    name = models.CharField(max_length=8, unique=False)
    numberID = models.CharField(max_length=5)
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)

    def __str__(self):
        return "{} of {} project({})".format(self.name, self.user, self.numberID)


# This class will define the Messages that sent from Phones to Server .
# Message : The Message . this can be anything . e.g : K_1 ( The Number one Key )
# User : The project . e.g : Mohammad's project
# Client : The client that this message is sent for it .  e.g : Lights Arduino with numer id :8
# Value : The Value of this message . it will be the command . e.g : 1 or 0 ( turn it on or off )
# isRead : a Bool arg that shows this message is read or not , it will cause a message dont launch for two or zero time .
# time : When this message is sent ? whe get this because we should clear history of DB after a while .

class MessageFromDevice(models.Model):
    message = models.CharField(max_length=11, null=False)
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    value = models.CharField(max_length=10)
    isRead = models.BooleanField(default=False)
    time = models.DateTimeField()

    def __str__(self):
        return "{} Say : {} : {} To {}".format(self.user, self.message, self.value, self.client)

# This class defines every projects .
# User Name : this will be used for login . e.g : Mohammad
# Token : This will be used for each messages to make sure the message is come from correct device and will be send to correct devise . this  is a 48 char HASHED string .
# Project ID : this will be used to find the project in DB . e.g : 1234567
# Password : this will be used for login . e.g : 1482326


class UserInfo(models.Model):
    userName = models.CharField(max_length=30)
    token = models.CharField(max_length=48, null=False)
    projectId = models.CharField(max_length=11)
    password = models.CharField(max_length=24)
    configs = models.TextField(default="")

    def __str__(self):
        return "{} - {} ".format(self.userName, self.projectId)


class MessageFromClient(object):
    message = models.CharField(max_length=11, null=False)
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    value = models.CharField(max_length=10)
    isRead = models.BooleanField(default=False)
    time = models.DateTimeField()

    def __str__(self):
        return "{} Say : {} : {} To {}".format(self.user, self.message, self.value, self.client)
