"""JJnovel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Novelweb import views
from django.conf.urls.static import static
from django.conf import settings
import xadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/',xadmin.site.urls),
    path('',views.home),
    path('library/',views.library),
    path('rank/',views.rank),
    path('register/',views.register),
    path('author/',views.makeAuthor),
    path('login/',views.login),

    path('user/<int:userid>/',views.UserInfo),
    path('author/<int:authorid>/',views.authorInfo),

    path('mycreate/',views.createBookList),
    path('create_book/',views.createBook),
    path('mycreate/<int:bid>/',views.authorBookInfo),
    path('mycreate/<int:bid>/addchapter/',views.addChapter),
    path('mycreate/<int:bid>/edit_chapter/<int:chapterid>/',views.editChapter),
    path('mycreate/<int:bid>/pub_chapter/<int:chapterid>/',views.pubChapter),
    path('mycreate/<int:bid>/bookpub/',views.Book_pub),
    path('<int:chapterid>/makeprice/',views.makePrice),
    path('<int:bid>/endbook/',views.endBook),
    path('del_book/',views.delBook),
    path('money/',views.Income),
    path('<int:aid>/cashout/',views.cashOut),
    path('delcomment/<int:commid>/',views.delComment),
    path('mycreate/<int:bid>/pubnotice/',views.pubNotice),

    # path('book/',views.bookList),
    path('book/<int:bid>/',views.BookInfo),
    path('reply/<int:bid>/<int:commentid>/',views.Reply),
    path('<int:bid>/chapters/',views.Chapters),
    path('<int:bid>/<int:chapterid>/',views.bookRead),
    path('rack/',views.Rack),
    path('book/<int:bid>/collect/',views.Collect),
    path('book/<int:bid>/uncollect/',views.unCollect),
    path('book/<int:bid>/recommend/',views.Recommend),
    path('book/<int:bid>/gif/',views.Gif),
    path('<int:chapterid>/pay_chapter/',views.payChapter),
    path('<int:aid>/works/',views.autWorks),

    path('pay/',views.Pay),
    path('updateorder/',views.update_order),
    path('pay_record/',views.payRecord),
    path('updateinfo/',views.updateInfo),


    # path('user_update/',views.UserInfo),
    # path('edit_avatar/',views.edit_avatar),

    path('logout/',views.log_out),
    path('serach/',views.Serach),


]

urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
