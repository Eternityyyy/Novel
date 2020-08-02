from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from Novelweb.models import User,Author,Book,Comment,Chapter,Bookrack,Code,OrderInfo,CashoutInfo
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Novelweb.alipay import Alipay
from urllib.parse import parse_qs
from django.conf import settings
from decimal import *

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore,register_events,register_job

import time
import re
import math

# 定义定时器,用于每天凌晨更新用户的推荐票
try:
	scheduler = BackgroundScheduler()#创建一个调度器
	scheduler.add_jobstore(DjangoJobStore(),'default')
	@register_job(scheduler,'cron',day_of_week='0-6',hour='0',minute='0',second='0')
	def time_task():
		users= User.objects.all()
		for user in users:
			user.day_ticket_num = int(math.log(user.user_level,10))
			user.save()
	register_events(scheduler)
	scheduler.start()
except Exception as e:
	print(e)
	scheduler.shutdown()
# 触发器：date：特定的时间点触发执行一次；interval:固定时间间隔触发；cron：在特定的时间周期性触发，执行多次。job也可移除

# Create your views here.

# 主页
def home(request):
	# 查出所有上架的书籍
	books = Book.objects.all().filter(Book_pub = True)
	# 精品重推的书籍
	most_books = books.order_by('-chapterIncome')[:8]

	type_ancients = books.filter(Book_type = '古代言情')[:8]
	type_ancients_big = type_ancients[0]
	type_ancients_middle = type_ancients[1:4]
	type_ancients_small = type_ancients[4:8]

	type_moderns = books.filter(Book_type = '现代言情')[:8]
	type_moderns_big = type_moderns[0]
	type_moderns_middle = type_moderns[1:4]
	type_moderns_small = type_moderns[4:8]

	# 新书上架的书
	new_books = books.order_by('-Book_time')[:6]

	# 找出最近更新
	late_chapters = {}
	chapters = Chapter.objects.all().order_by('-Chapter_time')[:100]
	for chapter in chapters:
		if chapter.Chapter_book.Book_name not in late_chapters:
			late_chapters[chapter.Chapter_book.Book_name] = chapter
		if len(late_chapters)>30:
			break

	# print('.............',len(late_chapters))

	# 排行榜的书籍
	money_books = books.order_by('-Income')[:10]
	sub_books = books.order_by('-chapterIncome')[:10]
	rec_books = books.order_by('-recommend_num')[:10]
	banner_books = books.filter(Q(id__gt=179)&Q(id__lt = 186))

	return render(request,'index.html',{
		'most_books':most_books,
		'type_ancients_big':type_ancients_big,
		'type_ancients_middle':type_ancients_middle,
		'type_ancients_small':type_ancients_small,
		'type_moderns_big':type_moderns_big,
		'type_moderns_middle':type_moderns_middle,
		'type_moderns_small':type_moderns_small,
		'new_books':new_books,
		'late_chapters':late_chapters,
		'money_books':money_books,
		'sub_books':sub_books,
		'rec_books':rec_books,
		'banner_books':banner_books,
		})
	pass

# 书库界面的处理函数
def library(request):
	book_types=['古代言情','仙侠奇缘','现代言情','浪漫青春','玄幻言情','悬疑推理','游戏竞技','轻小说','科幻空间']
	books = Book.objects.all().filter(Book_pub = True)
	money_books = books.order_by('-Income')[:10]

	if request.GET.get('category'):
		books = books.filter(Book_type = book_types[int(request.GET['category'])])
	if request.GET.get('state'):
		books = books.filter(Book_state = request.GET['state'])
	if request.GET.get('order'):
		order_way = ['-Click_num','-Collect_num','-recommend_num','-chapterIncome']
		books = books.order_by(order_way[int(request.GET['order'])])

	paginator = Paginator(books,15)
	page_number = request.GET.get('page',1)
	pagebooks = paginator.get_page(page_number)

	return render(request,'library.html',{
		'money_books':money_books,
		'pagebooks':pagebooks,
		})
	pass

# 处理排行榜的函数
def rank(request):
	books = Book.objects.all().filter(Book_pub = True)
	money_books = books.order_by('-Income')
	collect_books = books.order_by('-Collect_num')
	rec_books = books.order_by('-recommend_num')
	sub_books = books.order_by('-chapterIncome')
	gif_books = books.order_by('-Git_num')
	click_books = books.order_by('-Click_num')
	all_rank = [money_books,collect_books,rec_books,sub_books,gif_books,click_books]
	if request.GET.get('rank'):
		return render(request,'rank-list.html',{'ranks':all_rank[int(request.GET['rank'])][:50]})
		pass
	return render(request,'rank.html',{
		'money_books':money_books[:10],
		'collect_books':collect_books[:10],
		'rec_books':rec_books[:10],
		'sub_books':sub_books[:10],
		'gif_books':gif_books[:10],
		'click_books':click_books[:10],
		})

# 作者的所有上架书籍显示
def autWorks(request,aid):
	works = Book.objects.filter(Aut_user_id =aid).filter(Book_pub = True);
	return render(request,'authorbooks.html',{'works':works})

# 跨站攻击的注释器,书籍详情页的处理函数
@csrf_exempt
def BookInfo(request,bid):
	# 书籍评论功能
	if request.POST:
		comment_text = request.POST.get('commenttext')
		Comment.objects.create(
			Comment_user = User.objects.get(id = request.session['uid']),
			Comment_book = Book.objects.get(id = bid),
			Comment_text = comment_text,
			)
		comment = Comment.objects.get(Comment_text = comment_text)
		return redirect('/book/%s/'%bid)
	books = Book.objects.all().filter(Book_pub = True)
	book = books.get(id = bid)
	book.Click_num = book.Click_num+1
	book.save()
	collectstatus = False
	# 显示收藏的状态
	if 'uid' in request.session:
		if Bookrack.objects.filter(Bookrack_user_id = request.session['uid']).filter(Bookrack_book_id = bid):
			collectstatus = True
	comments = Comment.objects.filter(Q(Comment_book = book)&Q(reply = None))
	replys_dict = {}
	# 所有回复
	for comment in comments:
		replys = Comment.objects.filter(reply = comment)
		replys_dict[comment.id] = replys
	money_books = books.order_by('-Income')[:10]
	other_books = books.filter(Book_author = book.Book_author).filter(Book_pub = True)[:2]
	type_books = books.filter(Book_type = book.Book_type).order_by('-Income')[:10]

	chapters = Chapter.objects.filter(Chapter_book = book)
	chapter = chapters.order_by('-Chapter_time').first()
	tags = book.Book_tags.split('、')
	tags.pop()
	return render(request,'book.html',{
		'book':book,
		'comments':comments,
		'chapter':chapter,
		'replys_dict':replys_dict,
		'collectstatus':collectstatus,
		'tags':tags,
		'money_books':money_books,
		'other_books':other_books,
		'type_books':type_books,
		})
# @csrf_exempt
# 实现收藏功能
def Collect(request,bid):
	userid = request.session['uid']
	book = Book.objects.get(id = bid)
	user = User.objects.get(id = userid)
	Bookrack.objects.create(
		Bookrack_user = user,
		Bookrack_book = book,
		)
	book =Book.objects.get(id = bid)
	book.Collect_num = book.Collect_num+1
	book.save()
	return JsonResponse({'collect_num':book.Collect_num})

# 取消收藏
# @csrf_exempt
def unCollect(request,bid):
	userid = request.session['uid']
	Bookrack.objects.filter(Bookrack_user_id = userid).filter(Bookrack_book_id = bid).delete()
	book =Book.objects.get(id = bid)
	book.Collect_num = book.Collect_num-1
	book.save()
	return JsonResponse({'collect_num':book.Collect_num})

# 投推荐票
def Recommend(request,bid):
	userid = request.session['uid']
	user = User.objects.get(id = userid)
	if user.day_ticket_num<=0:
		return JsonResponse({'recommend':False})
		pass
	user.day_ticket_num = user.day_ticket_num - 1
	user.save()
	book = Book.objects.get(id = bid)
	book.recommend_num = book.recommend_num + 1
	book.save()
	return JsonResponse({'recommend':book.recommend_num})

# 送礼,也算收入
def Gif(request,bid):
	userid = request.session['uid']
	user = User.objects.get(id = userid)
	if user.gold-100<0:
		return JsonResponse({'gold':False})
	user.gold = user.gold - 100
	user.save()
	print(user.gold)
	book = Book.objects.get(id = bid)
	book.Git_num = book.Git_num +1
	book.Income = book.Income + 100
	book.save()
	book.Book_author.Income += Decimal.from_float(1.00)
	book.Book_author.save()
	return JsonResponse({'gif':book.Git_num})
	pass

# 实现回复功能
def Reply(request,bid,commentid):
	if request.POST:
		reply_text = request.POST.get('commenttext')
		Comment.objects.create(
			Comment_user = User.objects.get(id = request.session['uid']),
			Comment_book = Book.objects.get(id = bid),
			Comment_text = reply_text,
			reply = Comment.objects.get(id = commentid)
			)
		return redirect('/book/%s/'%bid)

# 目录页
def Chapters(request,bid):
	chapters = Chapter.objects.filter(Chapter_book_id = bid).order_by('Chapter_id')
	book = Book.objects.get(id = bid)

	return render(request,'chapters.html',{'chapters':chapters,'book':book})

# 章节内容显示页
def bookRead(request,bid,chapterid):
	try:
		chapter = Chapter.objects.filter(Chapter_book_id = bid).get(Chapter_id = chapterid)
	except Exception as e:
		return redirect('/%s/chapters/'%bid)

	return render(request,'book-read.html',{'chapter':chapter,'bookid':bid})

# 实现买章节
def payChapter(request,chapterid):
	buyuser = User.objects.get(id = request.session['uid'])
	chapter = Chapter.objects.get(id = chapterid)
	buyuser.gold -=chapter.Chapter_price
	buyuser.save()
	chapter.buy_user.add(buyuser)
	chapter.save()
	chapter.Chapter_book.Income += chapter.Chapter_price
	chapter.Chapter_book.chapterIncome += chapter.Chapter_price
	chapter.Chapter_book.save()
	chapter.Chapter_book.Book_author.Income += Decimal.from_float(float(chapter.Chapter_price/100))
	# 浮点型转换为decimal类型进行计算
	chapter.Chapter_book.Book_author.save()
	return redirect('/%s/%s/'%(chapter.Chapter_book_id,chapter.Chapter_id))

# 收入书架功能
@csrf_exempt
def Rack(request):
	# if request.is_ajax():
	# 	bookid = request.POST.get('bookid')
	# 	userid = request.session['uid']
	# 	if Bookrack.objects.filter(Bookrack_user_id = userid).filter(Bookrack_book_id = bookid):
	# 		return JsonResponse({'success':False})
	# 		pass
	# 	book = Book.objects.get(id = bookid)
	# 	user = User.objects.get(id = userid)
	# 	Bookrack.objects.create(
	# 		Bookrack_user = user,
	# 		Bookrack_book = book,
	# 		)
	# 	pass
	# 	return JsonResponse({'success':True})
	if 'uid' not in request.session:
		return redirect('/login/')
	userid = request.session['uid']
	bookracks = Bookrack.objects.filter(Bookrack_user_id = userid)
	return render(request,'author/rack.html',{'bookracks':bookracks})

# 
# def bookList(request):
# 	books = Book.objects.all();
# 	return render(request,'booklist.html',{'books':books})
# 	pass

# 注册
def register(request):
	if request.POST:
		if User.objects.all().exists():
			length = User.objects.count()
			userid = str(int(User.objects.all()[length-1].user_id) + 1)#取最后一个用户的账号加1成为新用户的账号
		else:
			userid = str(1000)
		User.objects.create(
			username = request.POST.get('username'),
			password = request.POST.get('pas'),
			user_id = userid,
			user_avatar = request.FILES.get('avatar','default.png'),
			user_level = 10,
			gold = 0,
			points = 0,
			day_ticket_num =1,
			Wine_num = 0,
			comment_level = 1,

			)
		return redirect('/login/')
	return render(request,'register.html')

# 登录
def login(request):
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('pas')
		
		try:
			user =User.objects.get(username = username)
		except User.DoesNotExist:
			return render(request,'login.html',{'error':'没有此用户'})

		if user.password == password:
			request.session['uid'] = user.id
			request.session['avatar'] =user.user_avatar.url
			request.session['username'] = user.username
			if Author.objects.filter(Aut_user = user).exists():
				request.session['aid'] = Author.objects.get(Aut_user = user).Aut_user_id
			return redirect('/user/%s/'%user.id)
		else:
			return render(request,'login.html',{'error':'密码错误'})

	else:
		return render(request,'login.html')

# 查看用户信息
@csrf_exempt
def UserInfo(request,userid):
	# user_id = request.GET.get('user_id')#bug:知道人家的ID号直接可以查看别人的信息
	if request.session.get('uid','') is '':
		return redirect('/login/')
	try:
		user = User.objects.get(id = request.session['uid'])
	except User.DoesNotExist:
		return redirect('/login/')

	# if request.POST:
	# 	username = request.POST.get('username')
	# 	User.objects.filter(id= request.session['uid']).update(username= username)
	# 	return JsonResponse({'username':username})
	# 	pass

	return render(request,'userinfo.html',{'user':user})

# 退出登录
def log_out(request):
	request.session.flush()
	return redirect('/')
	
# 修改用户信息有bug,还没想好怎么解决
@csrf_exempt
def updateInfo(request):
	if request.session.get('uid','') is '':
		return redirect('/login/')
	if request.POST:
		username = request.POST.get('username')
		pre_avatar = request.POST.get('pre_avatar')
		avatar = request.FILES.get('avatar',pre_avatar)
		up_user = User.objects.get(id = request.session.get('uid'))
		up_user.username = username
		up_user.user_avatar = avatar
		up_user.save()
		request.session['avatar'] = up_user.user_avatar.url
		if request.POST.get('penname'):
			author = Author.objects.get(Aut_user = up_user)
			author.penname = request.POST.get('penname')
			author.save()
			return redirect('/author/%s/'%author.Aut_user_id)
		return redirect('/user/%s/'%up_user.id)
	context = {}
	user = User.objects.get(id =request.session['uid'])
	context['user'] = user
	if request.session.get('aid','') is not '':
		context['author'] = Author.objects.get(Aut_user_id = request.session.get('aid'))
	return render(request,'author/updateinfo.html',context)
# def edit_avatar(request):
# 	if request.POST:
# 		user_avatar = request.FILES.get('file')
# 		# print(request.POST.get('num'))
# 		if user_avatar:
# 			User.objects.filter(id= request.session['uid']).update(user_avatar = user_avatar)
# 			return JsonResponse({'useravatar':User.objects.get(id = request.session['uid']).user_avatar.url})
# 	return redirect('/login/')

# 申请成为作者
def makeAuthor(request):
	if request.session.get('uid','') is '':
		return redirect('/login/')
	user = User.objects.get(id =request.session['uid'])
	if request.POST:
		penname = request.POST.get('penname')
		realname = request.POST.get('realname')
		phone = request.POST.get('phone')
		discript = request.POST.get('discript','')
		code_num = request.POST.get('code')
		try:
			code = Code.objects.get(code_num = code_num)
		except Code.DoesNotExist:
			return render(request,'author/author.html',{'error':'联系编辑获取注册码哟','user':user})
		author_user = User.objects.get(id = request.session['uid'])
		Author.objects.create(
			Aut_user = author_user,
			penname = penname,
			realname = realname,
			phone = phone,
			Author_info = discript,
			)
		author = Author.objects.get(Aut_user = author_user)
		request.session['aid'] = author.Aut_user_id
		print(request.session['aid'])
		return redirect('/author/%s/'%author.Aut_user_id)
	return render(request,'author/author.html',{'user':user})

# 显示作者信息
def authorInfo(request,authorid):
	if request.session.get('aid','') is '':
		return redirect('/author/')
	author = Author.objects.get(Aut_user_id = request.session['aid'])
	return render(request,'author_info.html',{'author':author})

# 作者创的书籍所有书籍
def createBookList(request):
	if request.session.get('aid','') is '':
		return redirect('/author/')
	books = Book.objects.filter(Book_author = Author.objects.get(Aut_user_id = request.session['aid']))
	return render(request,'author/authorbooks.html',{'books':books})

# 创建书籍
def createBook(request):
	if request.session.get('aid','') is '':
		return redirect('/author/')
	if request.POST:
		bookname = request.POST.get('bookname')
		bookcover = request.FILES.get('cover','cover.png')
		booktype = request.POST.get('type')
		booktags = request.POST.getlist('tags')
		bookintro = request.POST.get('bookintro')
		manleader = request.POST.get('manleader')
		womanleader = request.POST.get('womanleader')
		if booktype == '':
			booktype = '其他'
		if bookintro == '':
			bookintro = '暂无简介'
		Booktags = ''
		if booktags:
			for booktag in booktags:
				Booktags =Booktags + booktag + '、'
		else:
			booktags = '其它'
		try:
			author = Author.objects.get(Aut_user_id = request.session['aid'])
		except DoesNotExist:
			return redirect('/author/')
		Book.objects.create(
			Book_author = author,
			Book_name = bookname,
			Book_type = booktype,
			Book_intro = re.sub(r'\n|\t','<br/>',bookintro),
			Book_tags = Booktags,
			Book_cover = bookcover,
			Book_manleader = manleader,
			Book_womanleader = womanleader,
			Book_pub = False,
			Book_notice = '暂无公告',
			Click_num = 0,
			Collect_num = 0,
			Income = 0,
			Git_num = 0,
			chapterIncome =0,
			recommend_num = 0,
			Book_state = False,
			)
		book = Book.objects.filter(Book_author = author).last()
		return redirect('/mycreate/%s/'%book.id)
	return render(request,'author/createbook.html')

# 发布公告
@csrf_exempt
def pubNotice(request,bid):
	notice = request.POST.get('notice')
	Book.objects.filter(id = bid).update(Book_notice = notice)
	return JsonResponse({'pubnotice':True})

# 作者的书籍信息
def authorBookInfo(request,bid):
	book = Book.objects.get(id = bid)
	chapters = Chapter.objects.filter( Chapter_book = book).order_by('Chapter_id')
	comments = Comment.objects.filter(Comment_book = book)
	bookdata = [book.Click_num,book.Collect_num,book.Git_num,book.recommend_num]
	return render(request,'author/bookinfo.html',{'book':book,'chapters':chapters,'comments':comments})

# 书籍的发布功能
def Book_pub(request,bid):
	book = Book.objects.get(id = bid)
	book.Book_pub = not book.Book_pub
	book.save()
	print(book.Book_pub)
	return JsonResponse({'book_status':book.Book_pub})

# 指定价格
@csrf_exempt
def makePrice(request,chapterid):
	Chapter.objects.filter(id = chapterid).update(Chapter_price = request.POST.get('price'))
	return JsonResponse({'price':True})
# 完结书籍
def endBook(request,bid):
	Book.objects.filter(id = bid).update(Book_state = True)
	return JsonResponse({'bookstate':True})

# 添加章节
def addChapter(request,bid):
	if request.POST:
		chaptertitle = request.POST.get('chapter_name','')
		chaptertext= request.POST.get('chapter_text','')
		book = Book.objects.get(id = bid)
		chapter_num = Chapter.objects.filter(Chapter_book = book).count()+1
		Chaptertitle = '第 %d 章 %s'%(chapter_num,chaptertitle)
		Chapter.objects.create(
			Chapter_book = book,
			Chapter_id = chapter_num,
			Chapter_title = Chaptertitle,
			Chapter_text = re.sub(r'\n|\t','<br/>',chaptertext),
			Chapter_pub = False,
			Chapter_word_num = len(chaptertext),
			Chapter_price = 0,
			)
		return redirect('/mycreate/%s/'%bid)

	return render(request,'author/addchapter.html',{'bookid':bid})

# 编辑章节
@csrf_exempt
def editChapter(request,bid,chapterid):
	if request.POST:
		chaptertext = request.POST.get('chaptercontent')
		# chaptertext = re.sub(r'<br/*>',chr(10),chaptertext)
		chapter = Chapter.objects.get(id = chapterid)
		chapter.Chapter_text = chaptertext
		chapter.Chapter_word_num = len(re.sub(r'&nbsp;*|<br/*>|</*p>','',chaptertext))
		chapter.Chapter_pub = False
		chapter.save()
		print(chapter.Chapter_text)
		return JsonResponse({'chaptercontent':chapter.Chapter_text,'wordnum':chapter.Chapter_word_num})	

# 发布章节
def pubChapter(request,bid,chapterid):
	chapter = Chapter.objects.get(id = chapterid)
	chapter.Chapter_pub = True
	chapter.save()
	print(chapter.Chapter_pub)
	return JsonResponse({'chapterpub':chapter.Chapter_pub})

# 删除评论
def delComment(request,commid):
	try:
		Comment.objects.filter(id = commid).delete()
		return JsonResponse({'delcomment':True})
	except Exception as e:
		return JsonResponse({'delcomment':False})

# 删除书籍
def delBook(request):
	bookid = request.GET.get('book_id')
	Book.objects.filter(id = bookid).delete()
	return redirect('/manage_book/')
# 收入
def Income(request):
	author = Author.objects.get(Aut_user_id = request.session['aid'])
	books = Book.objects.filter(Book_author = author)
	cashouts = CashoutInfo.objects.filter(Cashout_aut = author)
	return render(request,'author/economy.html',{'books':books,'cashouts':cashouts,'author':author})

# 提现
def cashOut(request,aid):
	if request.POST:
		cash = Decimal.from_float(float(request.POST.get('cash')))
		CashoutInfo.objects.create(
			Cashout_aut_id = aid,
			Cash_status = 'TRADE_WAIT',
			Cash_count = cash,
			)
		author = Author.objects.get(Aut_user_id = aid)
		author.Income -=cash
		author.save()
	return redirect('/money/')

# 阿里云支付实例化
def aliPay():
	obj = Alipay(
		appid = '2016101700709591',
		app_notify_url='http://127.0.0.1:8000/updateorder/',#如果支付成功，会向这个地址发送post请求，校验是否支付成功
		return_url = 'http://127.0.0.1:8000/updateorder/',#如果支付成功会重定向到这里
		alipay_public_key_path = settings.ALIPAY_PUBLIC,
		app_private_key_path = settings.APP_PRIVATE,
		debug = True
		)
	return obj

# 支付功能
@csrf_exempt
def Pay(request):
	if 'uid' not in request.session:
		return redirect('/login/')
		pass
	if request.method == 'GET':
		return render(request,'pay.html')

	# 实例化sdk中的类Alipay
	alipay = aliPay()
	# 对购买的数据进行加密
	money = float(request.POST.get('price'))#保留两位小数，前端传来的数据
	out_trade_no ='jj'+str(time.time())#商户订单号，可更具自己的的爱好生成订单
	OrderInfo.objects.create(
		Order_user_id = request.session['uid'],
		Order_sn = out_trade_no,
		order_mount = money,
		pay_status = 'WAIT_BUYER_PAY'

		)

	query_params = alipay.direct_pay(
		subject='金币充值',#用于商品描述，可前端传递过来
		out_trade_no=out_trade_no,#商户订单号
		total_amount=money,#交易金额

		)
	pay_url = 'https://openapi.alipaydev.com/gateway.do?{}'.format(query_params)
	print(pay_url)

	return redirect(pay_url)

@csrf_exempt
def update_order(request):
	# 支付成功进行验证
	body_str = request.body.decode('utf-8')
	get_data = request.GET.dict()

	alipay = aliPay()
	sign = get_data.pop('sign',None)
	status = alipay.verify(get_data,sign)
	if status:
		out_trade_no = get_data.get('out_trade_no')
		order = OrderInfo.objects.get(Order_sn=out_trade_no)
		rmb = order.order_mount
		money = int(rmb)
		order.Order_user.gold +=(money*100)
		order.Order_user.user_level +=(money*100)
		order.Order_user.save()
		order.pay_status = 'TRADE_SUCCESS'
		order.save()

	# return HttpResponse('success')
	return redirect('/user/%s/'%request.session['uid'])

# 支付记录
def payRecord(request):
	orders = OrderInfo.objects.filter(Order_user_id = request.session['uid'])
	return render(request,'author/payrecord.html',{'orders':orders})
# 搜索功能
def Serach(request):
	context = {}
	if request.POST:
		key_word = request.POST.get('serach')
		books = Book.objects.all()
		serachs = books.filter(Q(Book_name__contains = key_word)|Q(Book_author__penname__contains = key_word)|Q(Book_manleader__contains = key_word)|Q(Book_womanleader__contains = key_word)|Q(Book_tags__contains = key_word))
		context['serachs']=serachs
	return render(request,'serachs.html',context)
