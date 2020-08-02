from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from base64 import decodebytes,encodebytes
import json
# 这个Apliay类只要是用来生成一个包含订单详情、签名的大字典，然后把这个大字典加密成字符串凭借到支付宝付款网关接口路径后后面
# 视图中重定向到改地址，支付宝处理完成后向我们的路由发get请求携带详细信息和签名，使用这个类的方法来校验签名即可
class Alipay(object):
	# 支付宝支付接口（pc端支付接口）初始化设置

	def __init__(self,appid,app_notify_url,app_private_key_path,alipay_public_key_path,return_url,debug=False):
		self.appid = appid
		self.app_notify_url = app_notify_url
		self.app_private_key_path = app_private_key_path
		self.app_private_key = None
		self.return_url = return_url
		# 打开应用私钥文件获取私钥
		with open(self.app_private_key_path) as fp:
			self.app_private_key = RSA.importKey(fp.read())

		# 打开应用公钥文件获取公钥
		self.alipay_public_key_path = alipay_public_key_path
		with open(self.alipay_public_key_path) as fp:
			self.alipay_public_key = RSA.importKey(fp.read())

		if debug:
			# 如果是沙箱测试就是这个网关
			self.__gateway = "https://openapi.alipaydev.com/gateway.do"
		else:
			self.__gateway = "https://openapi.alipay.com/gateway.do"

	def direct_pay(self,subject,out_trade_no,total_amount,return_url=None,**kwargs):
		biz_content = {
		'subject':subject,
		'out_trade_no':out_trade_no,
		'total_amount':total_amount,
		'product_code':'FAST_INSTANT_TRADE_PAY',

		}
		biz_content.update(kwargs)
		data = self.bulid_body('alipay.trade.page.pay',biz_content,self.return_url)
		return self.sign_data(data)

	def bulid_body(self,method,biz_content,return_url=None):
		data = {
		'app_id':self.appid,
		'method':method,
		'charset':'utf-8',
		'sign_type':'RSA2',
		'timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
		'version':'1.0',
		'biz_content':biz_content
		}

		if return_url is not None:
			data['notify_url'] = self.app_notify_url
			data['return_url'] = self.return_url

		return data

	def sign_data(self,data):
		data.pop('sign',None)

		unsigned_items = self.ordered_data(data)
		unsigned_string = '&'.join('{0}={1}'.format(k,v) for k,v in unsigned_items)
		sign = self.sign(unsigned_string.encode("utf-8"))
		quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)
		# 获取最终的订单信息字符串
		signed_string = quoted_string + '&sign='+quote_plus(sign)
		return signed_string

	def ordered_data(self,data):
		complex_keys = []
		for key,value in data.items():
			if isinstance(value,dict):
				complex_keys.append(key)

		# 将字典类型的数据dump出来
		for key in complex_keys:
			data[key] = json.dumps(data[key],separators=(',',':'))

		return sorted([(k,v) for k,v in data.items()])

	def sign(self,unsigned_string):
		# 开始计算签名
		key = self.app_private_key
		signer = PKCS1_v1_5.new(key)
		signature = signer.sign(SHA256.new(unsigned_string))
		# base64编码，转换为unicode表示并移除会回车
		sign = encodebytes(signature).decode('utf8').replace('\n','')
		return sign

	def __verify(self,raw_content,signature):
		# 开始计算签名
		key = self.alipay_public_key
		signer = PKCS1_v1_5.new(key)
		digest = SHA256.new()
		digest.update(raw_content.encode('utf8'))
		if signer.verify(digest,decodebytes(signature.encode('utf8'))):
			return True

		return False

	def verify(self,data,signature):
		if 'sign_type' in data:
			sign_type = data.pop('sign_type')
		unsigned_items = self.ordered_data(data)
		message = '&'.join(u'{}={}'.format(k,v) for k,v in unsigned_items)
		return self.__verify(message,signature) 
