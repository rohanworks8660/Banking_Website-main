from django.contrib import admin

# Register your models here.


from profiles.models import UserInfo


admin.site.register(UserInfo)
