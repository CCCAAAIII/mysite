from django.contrib import admin
from . import models


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    # 列表页面要显示的属性
    list_display = ['email', 'username']
    # 过滤的属性
    list_filter = ['email']
    #分页的数量
    list_per_page = 2

    #修改的属性
    fields = ['username']

    #位置 action
    actions_on_bottom = True
    actions_on_top = False




admin.site.register(models.User, UserAdmin)
admin.site.register(models.Article)
