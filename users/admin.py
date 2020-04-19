from django.contrib import admin

# Register your models here.
from .  import  models

class UserAdmin(admin.ModelAdmin):
    list_display = ('nick_name','username','mobile','email')
    search_fields = ('nick_name','username')
    list_filter = ('last_login',)

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('用户信息',  {'fields': ['avatar','username', 'password']}),
        ('个人信息',  {'fields': ['nick_name', 'email', 'mobile']}),
        ('状态',      {'fields': ['is_active']}),
        ('登录状态',  {'fields': ['date_joined', 'last_login']}),
        ('个人权限',{'fields':["is_superuser","is_staff"]})
    ]


admin.site.register(models.User_Info,UserAdmin)
admin.site.register(models.FriendsApplication)


