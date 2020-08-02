var code ; //在全局定义验证码   
var codeflag = false; 
var code_box = document.querySelector(".code_box");
// 接着读的功能
// 文档加载完成就判断是否为章节界面，如果是直接存储章节的url，并把href修改掉
window.onload = function(){
	let reg = /^(\/(\d+\/){2})/;
	if (reg.test(window.location.pathname)) {
		localStorage.setItem("pre-url",window.location.pathname);
	}
	if (localStorage.getItem('pre-url')) {
		document.querySelector('.continue').setAttribute("href",localStorage.getItem('pre-url'));
	}
}
function isError(error_text,item_box,flag){//验证是否显示错误信息
	if (error_text !="") {
		flag = false;
		if (item_box.querySelector("p")==null) {
			let error_p =document.createElement("P");
			error_p.appendChild(document.createTextNode(error_text));
			item_box.appendChild(error_p);
		}
		else
			item_box.querySelector("p").innerHTML=error_text;
	}
	else{
		flag = true;
		if (item_box.querySelector("p")!=null) {
			item_box.removeChild(item_box.querySelector("p"));
		}
	}
	return flag;
		
}
function createCode(){ 
	code = "";  
	var codeLength = 4;//验证码的长度  
	var checkCode = document.querySelector(".code-img");  
	var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R',  
	                     'S','T','U','V','W','X','Y','Z');//随机数  
	for(var i = 0; i < codeLength; i++) {//循环操作  
	var index = Math.floor(Math.random()*35);//取得随机数的索引（0~34）  
	code += random[index];//根据索引取得随机数加到code上  
	}  
  checkCode.innerHTML = code;//把code值赋给验证码  
} 
//校验验证码 
function validateCode(){
	let error_message="";
	let inputCode = code_box.querySelector("input").value.toUpperCase();
	if (inputCode.length<=0) {
		error_message = "请输入验证码";
	}
	else if (inputCode !=code) {
		error_message = "验证码输入错误";
	}
	codeflag = isError(error_message,code_box,codeflag);
}

// 展示错误信息
function showmessage(mess){
	let message_ele = $('<span class="showmessage">'+mess+'</span>');
	console.log(message_ele);
	$('body').append(message_ele);
	window.setTimeout(function(){
		message_ele.remove();;
	},2000);
}
// 书库点击种类修改样式
$(function(){
	pre_url = window.location.search;
	if (pre_url.length>1) {
		console.log(pre_url);
		pre_url_arr = pre_url.split('?')[1].split('&');
		console.log(pre_url_arr);
		$('.a-link a').each(function(value,item){
			$(item).removeClass('condition-active');
				if(pre_url_arr.some(function(url_item){
					return url_item == $(item).attr('data-condition');
				})){
					$(item).addClass('condition-active');
				}
		})
	}
});