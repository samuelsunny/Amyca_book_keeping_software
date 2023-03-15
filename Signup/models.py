from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    businessName = models.CharField(max_length=100, null=True)
    contactNumber = models.CharField(max_length=20, null=True)
    subscriptionId = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "users"

class Subscriptions(models.Model):
    subscriptionId = models.AutoField(primary_key=True)
    userId = models.CharField(max_length=100, null=True)
    planType = models.CharField(max_length=100, null=True)
    paymentMethod = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "subscriptions"