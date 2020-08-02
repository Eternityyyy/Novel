from django.db import models

# Create your models here.
# 创建用户模型
class User(models.Model):
	user_id = models.CharField(max_length = 30,unique = True,verbose_name = '用户账号')
	username = models.CharField(max_length = 50,unique = True,verbose_name = '用户名')
	password = models.CharField(max_length = 120,verbose_name = '密码')
	user_avatar = models.ImageField(null = True,verbose_name = '用户头像')
	user_level = models.PositiveIntegerField(verbose_name = '等级')
	gold = models.PositiveIntegerField(verbose_name = '金币')
	points = models.PositiveIntegerField(verbose_name = '积分')
	day_ticket_num = models.PositiveIntegerField(verbose_name = '推荐票数')
	Wine_num = models.PositiveSmallIntegerField(verbose_name = '礼物拥有量')
	comment_level = models.PositiveSmallIntegerField(verbose_name = '评论等级')
	register_time = models.DateTimeField(auto_now_add = True,verbose_name = '注册时间')
	def __str__(self):
		return self.username
	class Meta:
		verbose_name = '用户'

# 创建作者模型,与作者一对一
class Author(models.Model):
	Aut_user = models.OneToOneField(User,on_delete = models.CASCADE,primary_key = True)
	realname = models.CharField(max_length = 20,verbose_name = '真实姓名')
	penname = models.CharField(max_length = 50,verbose_name = '笔名')
	phone = models.CharField(max_length = 15,verbose_name = '电话')
	Author_info = models.TextField(verbose_name = '作者信息')
	aliPay_num = models.CharField(max_length = 50,verbose_name = '支付宝账号')
	Income = models.DecimalField(verbose_name='总收入',max_digits=10,decimal_places=2,default=0.00)
	def __str__(self):
		return self.Aut_user.username

	class Meta:
		verbose_name = '作者'
	
# 创建书籍模型
class Book(models.Model):
	Book_author = models.ForeignKey(Author,on_delete = models.CASCADE)
	Book_name = models.CharField(max_length = 50,verbose_name = '书名')
	Book_type = models.CharField(max_length = 20,verbose_name ='类型')
	Book_tags = models.CharField(max_length = 50,verbose_name = '标签')
	Book_cover = models.ImageField(null = True,verbose_name = '封面')
	Book_intro = models.TextField(verbose_name = '简介')
	Book_manleader = models.CharField(max_length = 20,verbose_name = '男主')
	Book_womanleader = models.CharField(max_length = 30,verbose_name = '女主')
	Click_num = models.PositiveIntegerField(verbose_name = '点击量')
	Collect_num = models.PositiveIntegerField(verbose_name = '收藏量')
	Income = models.PositiveIntegerField(verbose_name ='收入')
	chapterIncome = models.PositiveIntegerField(verbose_name = '章节订阅')
	Git_num = models.PositiveIntegerField(verbose_name = '礼物量')
	recommend_num = models.PositiveIntegerField(verbose_name = '推荐票量')
	Book_state = models.BooleanField(verbose_name = '状态')
	Book_pub = models.BooleanField(verbose_name = '书籍发布状态')
	Book_notice = models.TextField(verbose_name = '作者公告')
	Book_time = models.DateField(auto_now_add = True,verbose_name = '创建时间')
	def __str__(self):
		return self.Book_name
	
	class Meta:
		verbose_name = '书籍'
# 创建评价模型
class Comment(models.Model):
	Comment_user = models.ForeignKey(User,on_delete = models.CASCADE)
	Comment_book = models.ForeignKey(Book,on_delete = models.CASCADE,null=True)
	Comment_text = models.TextField(verbose_name = '评论内容')
	Comment_time = models.DateTimeField(auto_now_add = True, verbose_name = '评论时间')
	reply = models.ForeignKey('self',on_delete = models.CASCADE,related_name = 'rp',null = True,blank = True)
	def __str__(self):
		return self.Comment_text
		pass
	
	pass
	class Meta:
		verbose_name = '评论'
# 创建章节模型
class Chapter(models.Model):
	Chapter_book = models.ForeignKey(Book,on_delete = models.CASCADE)
	Chapter_id = models.PositiveIntegerField(verbose_name='每本书的章节id')
	Chapter_title = models.CharField(max_length = 50,verbose_name = '章节标题')
	Chapter_text = models.TextField(verbose_name = '章节内容')
	Chapter_word_num = models.PositiveIntegerField(verbose_name = '章节字数')
	Chapter_price = models.PositiveSmallIntegerField(verbose_name = '价格')
	Chapter_pub = models.BooleanField(verbose_name = '章节发布状态')
	Chapter_time = models.DateTimeField(auto_now_add = True,verbose_name = '章节时间')
	buy_user = models.ManyToManyField(User,null = True,blank=True,default = None,verbose_name = '购买用户')
	def __str__(self):
		return self.Chapter_title
	class Meta:
		verbose_name = '章节'

# 创建书架模型
class Bookrack(models.Model):
	Bookrack_user = models.ForeignKey(User,on_delete = models.CASCADE)
	Bookrack_book = models.ForeignKey(Book,on_delete = models.CASCADE)

# 创建注册码模型,用于申请作者
class Code(models.Model):
	code_num = models.CharField(max_length = 10,verbose_name = '注册码')
	class Meta:
		verbose_name = '作者注册码'

# 创建订单记录模型
class OrderInfo(models.Model):
	ORDER_STATUS = (
		('TRADE_SUCCESS','交易支付成功'),
		('TRADE_CLOSED','未付款交易超时关闭'),
		('WAIT_BUYER_PAY','交易创建'),
		('TEADE_FINISHED','交易结束'),
		('paying','待支付'),
		)
	Order_user = models.ForeignKey(User,on_delete = models.CASCADE,verbose_name='用户')
	Order_sn = models.CharField(max_length=30,null = True,blank = True,verbose_name='订单号')
	pay_status = models.CharField(choices = ORDER_STATUS,max_length=40,verbose_name='支付状态')
	order_mount = models.DecimalField(verbose_name='充值金额',max_digits=10,decimal_places=2,default=0.00)
	Order_time = models.DateTimeField(auto_now_add = True,verbose_name='订单创建时间')

	def __str__(self):
		return self.Order_sn
	class Meta:
		verbose_name = '用户充值账单'

# 创建提现记录模型
class CashoutInfo(models.Model):
	CASH_STATUS = (
		('TRADE_SUCCESS','提现完成'),
		('TRADE_WAIT','待审核'),
		('TRADE_CLOSED','交易失败'),
		)
	Cashout_aut = models.ForeignKey(Author,on_delete = models.CASCADE,verbose_name='提现人')
	Cash_status = models.CharField(choices = CASH_STATUS,max_length = 40,verbose_name = '提现状态')
	Cash_count = models.DecimalField(max_digits=10,decimal_places = 2,default = 0.00,verbose_name='提现金额')
	Cashout_time = models.DateTimeField(auto_now_add = True,verbose_name = '提现时间')
	
	def __str__(self):
		return self.Cash_status
	class Meta:
		verbose_name = '作者提现记录'

		