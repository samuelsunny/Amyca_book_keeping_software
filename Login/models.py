from django.db import models

class Income(models.Model):
    incomeCategoryId  = models.AutoField(primary_key=True)
    incomeCategory  = models.CharField(max_length=100, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Income"

class Expense(models.Model):
    expenseCategoryId  = models.AutoField(primary_key=True)
    expenseCategory  = models.CharField(max_length=100, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "Expenses"

class Keywords(models.Model):
    wordId  = models.AutoField(primary_key=True)
    category  = models.CharField(max_length=100, null=True)
    categoryID  = models.CharField(max_length=100, null=True)
    sub_category  = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "Keywords"