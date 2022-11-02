from django.contrib import admin

# Register your models here.

from profiles.models import *

admin.site.register(UserInfo)
admin.site.register(Bills)
admin.site.register(ECS_Data)
admin.site.register(Money_Transfers)
admin.site.register(Transactions)
admin.site.register(Account_Data)
admin.site.register(Customer_Data)

