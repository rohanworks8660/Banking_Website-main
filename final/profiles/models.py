from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer_Data(models.Model):
    Cust_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Phone_no = models.CharField(max_length=10)
    # Fixed length can't be specified. Only max_length can be.
    Email = models.EmailField()
    #Username = models.CharField(max_length=30)
    #Password = models.CharField(max_length=30)
    #date_of_birth = models.DateField( blank=True, null=True)
    #address1 = models.CharField( max_length=1024, blank=True, null=True)

    class Meta:
        db_table = 'customer'


class Account_Data(models.Model):
    Accno = models.IntegerField(primary_key=True)
    Owner = models.ForeignKey(Customer_Data, on_delete=models.CASCADE)
    Balance = models.FloatField()
    #Name = models.CharField(max_length=200)

    class Meta:
        db_table = 'account'


'''    
class Deposits(models.Model): 
    Trans_ID = models.AutoField(primary_key=True)
    Accno = models.ForeignKey(Account, on_delete=models.CASCADE)
    Amount = models.FloatField()
    class Meta:
        db_table = 'deposits'
        
class Withdraws(models.Model): 
    Trans_ID = models.AutoField(primary_key=True)
    Accno = models.ForeignKey(Account, on_delete=models.CASCADE)
    Amount = models.FloatField()
    class Meta:
        db_table = 'withdraws' 
'''


class Transactions(models.Model):
    Trans_ID = models.AutoField(primary_key=True)
    Accno = models.ForeignKey(Account_Data, on_delete=models.CASCADE)
    Amount = models.FloatField()
    Type = models.CharField(max_length=30)
    # Type can be "withdraw" or "deposit"

    class Meta:
        db_table = 'transactions'


class Money_Transfers(models.Model):
    Trans_ID = models.AutoField(primary_key=True)
    From_accno = models.ForeignKey(
        Account_Data, on_delete=models.CASCADE, related_name='From_accno')
    To_accno = models.ForeignKey(
        Account_Data, on_delete=models.CASCADE, related_name='To_accno')
    Amount = models.FloatField()

    class Meta:
        db_table = 'transfers'


class ECS_Data(models.Model):
    ECS_ID = models.AutoField(primary_key=True)
    Payer_Name = models.CharField(max_length=300)
    Upper_Limit = models.FloatField()
    Account = models.ForeignKey(Account_Data, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ecs'


class Bills(models.Model):
    # id column created implicitly
    ECS_ID = models.ForeignKey(ECS_Data, on_delete=models.CASCADE)
    Amount = models.FloatField()
    Completed = models.BooleanField()

    class Meta:
        db_table = 'bills'


class UserInfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    fathers_name = models.CharField(max_length=100)
    mothers_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    dob = models.DateField()
    phone_number = models.IntegerField()
    email_address = models.EmailField()
    password = models.ForeignKey(
        User, on_delete=models.CASCADE, primary_key=True )
    class Meta:
        db_table = 'UserInfo'
