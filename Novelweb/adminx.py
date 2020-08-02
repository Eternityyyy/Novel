import xadmin
from xadmin import views

# Register your models here.
from Novelweb.models import User,Author,Book,Comment,Chapter,Bookrack,Code,OrderInfo,CashoutInfo

class GlobalSettings(object):
    site_title = "后台管理系统"
    site_footer = "后台管理系统"
    menu_style = "accordion"        # 设置收起菜单

# 启用xadmin主题功能
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class ShoeAdmin(object):
	style_fields ={'shoe_desc':'ueditor'}

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(User)
xadmin.site.register(Author)
xadmin.site.register(Book)
xadmin.site.register(Comment)	
xadmin.site.register(Chapter)
# admin.site.register(Bookrack, BookrackAdmin)
xadmin.site.register(Code)
xadmin.site.register(CashoutInfo)