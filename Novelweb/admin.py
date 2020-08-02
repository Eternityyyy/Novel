from django.contrib import admin

# Register your models here.
from Novelweb.models import User,Author,Book,Comment,Chapter,Bookrack,Code,OrderInfo,CashoutInfo

class UserAdmin(admin.ModelAdmin):
	list_display = ['user_id','username'] #管理员界面显示哪些列
	ordering = ['id'] #以id进行排序
	list_per_page = 50 #每页显示数量

class AuthorAdmin(admin.ModelAdmin):
	list_display = ['penname']
	list_per_page = 50

class BookAdmin(admin.ModelAdmin):
	list_display = ['Book_name','Income']
	odering = ['-Income']
	list_per_page = 50

class CommentAdmin(admin.ModelAdmin):
	list_display = ['Comment_text','Comment_book']
	list_per_page = 50

class ChapterAdmin(admin.ModelAdmin):
	list_display = ['Chapter_title','Chapter_book']
	list_per_page = 50

# class BookrackAdmin(admin.ModelAdmin):
# 	list_display = ['Bookrack_user']

class CodeAdmin(admin.ModelAdmin):
	list_display = ['code_num']
	list_per_page = 50

class CashoutInfoAdmin(admin.ModelAdmin):
	list_display = ['Cash_status']
	list_per_page = 50

# 注册管理员的model,添加之后管理员界面就能对数据进行操作
admin.site.register(User, UserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Comment, CommentAdmin)	
admin.site.register(Chapter, ChapterAdmin)
# admin.site.register(Bookrack, BookrackAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(CashoutInfo, CashoutInfoAdmin)	