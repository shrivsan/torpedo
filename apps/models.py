import datetime

from django.db import models
from rest_framework import serializers
import sys
import inspect

'''
Leave this Helper Class in the TOP of the file
'''

from django.contrib.auth.models import AbstractUser


class Utils:
    @staticmethod
    def get_class(config, name: str) -> models.Model:
        return Utils.model_name_to_class(config[name])

    @staticmethod
    def get_manager(config, name: str) -> models.Manager:
        return Utils.get_class(config, name).objects

    @staticmethod
    def get_serializer(config, name: str):
        class Serializer(serializers.ModelSerializer):
            class Meta:
                model = Utils.get_class(config, name)
                fields = '__all__'

        return Serializer

    @staticmethod
    def model_name_to_class(name: str):
        all_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        for cls in all_classes:
            if cls[0] == name:
                return cls[1]
        # we are confident that never returns None
        return None

'''
Add your models below
'''

class Organization(models.Model):
    name = models.CharField(max_length=254)

class User(AbstractUser):
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    email = models.EmailField(null=True,max_length=254)
    phone = models.PositiveIntegerField(null=True,default=0)
    first_name=models.CharField(null=True,max_length=254)
    last_name = models.CharField(null=True,max_length=254)
    role = models.CharField(null=True,max_length=20)
    is_active = models.BooleanField(default=True)
    status = models.CharField(null=True,max_length=20)
    org = models.ForeignKey(Organization, null=True,on_delete=models.PROTECT)
    timestamp = models.DateTimeField(default=datetime.datetime.now())

class Book(models.Model):
    class Meta:
        app_label = 'dyn_datatables'

    name = models.CharField(max_length=100)
