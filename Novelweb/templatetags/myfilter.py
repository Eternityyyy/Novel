from django import template
from ..models import Chapter,User
import math

register = template.Library()
# 找出书籍的最新一章
@register.filter
def latechapter(value):
	if value.chapter_set.all():
		return value.chapter_set.all().order_by('Chapter_id').last()
	return None
# 找出字典中的第几个
@register.filter
def select(value,num):
	return value.get(num)

# 得到数据的长度
@register.filter
def length(value):
	return len(value)

# 获取数据库中交易状态的文字，get_shuxingming_display()函数能获取choices的值
@register.filter
def paystatus(value):
	return value.get_pay_status_display()
	pass

# 获取提现状态的文字
@register.filter
def cashstatus(value):
	return value.get_Cash_status_display()

# 根据经验值计算等级
@register.filter
def level(value):
	return int(math.log(value,10))

# 获取用户的当前金币数
@register.filter
def gold(value):
	return User.objects.get(id = value).gold

# 判断当前用户是否为购买用户
@register.filter
def is_buy_user(value,num):
	flag = False
	if len(value.all())>0:
		for item in value.all():
			if item.id == num:
				flag = True
	return flag

# 计算书籍有多少字
@register.filter
def word(value):
	Book_word_num = 0
	book_chapters = value.chapter_set.all()
	if book_chapters:
		for book_chapter in book_chapters:
			Book_word_num += book_chapter.Chapter_word_num
	return Book_word_num

# @register.filter
# def filter_chapter(value):
# 	late_chapters ={}
# 	for item in value:
# 		late_chapters[item.Chapter_book.Book_name] = item

# 		if len(late_chapters)>30:
# 			break

# 	return late_chapters
# 除法
@register.filter
def divi(value,num):
	return float(value/num)