// var avatar = document.querySelector(".uinfo-avatar").querySelector("input");
// var username = document.querySelector(".uinfo-level").querySelector("input");
var imageFile;
var formdata = new FormData();
var avatar = $('.uinfo-avatar input');
var bookid = $('.book-info-top img').attr('data-book');
var chapterid; 
var total_money = 0;
var style_tags = ['轻松','爆笑','虐恋','治愈','恶搞','生死','大爱','温馨','小白','宠文','唯美','暧昧',
			'励志','甜文','悲剧','铁血','爽文','苦恋','暗黑',
			'浪漫','HE','刺激','BG','GL','灵异','BL','历史','军事','体育',
			'未来','穿越','总裁','豪门','青葱','散文','冒险','职场','系统','剧本','虐文','历史','惊悚','重生']

var status_tgs = ['帝王','暴君','皇后','王妃','公主','王爷','将军','小妾','丫鬟','书童',
			'盗贼','王子','总裁','特工','世家','替身','黑帮','明星','纨绔','杀手',
			'职业','高手','老师','校花','校草','学生','女佣','佣兵','神医','毒医',
			'卧底','法师','僵尸','丧尸','精灵','魔女','才女','医生','兽人','丑女',]

var figure_tgs = ['扮猪吃虎','专情','花心','张扬','萌系','护短','可爱流','热血','玩世不恭','杀伐',
			'果断','宅腐','单纯','腹黑','傲娇','独宠','冰山','毒舌','逗逼','吃货',]

var story_tgs = ['魂穿','清穿','反穿越','学院','古娱','种田文','随身流','修仙','美食','盗墓',
			'鉴宝','宝宝','宠物','女强','复仇','争霸','契约','红楼','变身','转世',
			'系统流','废材流','养成','升级文','赌石','灵魂互换','出轨','宫斗权谋','婚恋']

var story_ele_tgs = ['青梅竹马','白领浪漫','策马江湖','乡村爱情','青楼宫廷','江湖恩怨','选秀','别后重逢','平凡','生活',
			'生活','麻雀变凤凰','家长里短','异国情缘','姐弟恋','暗恋成真','日久生情','欢喜冤家','乔装改扮','午夜惊魂',
			'裸婚','同居','待嫁','复合','军魂','生存奇遇']

var tags = new Map([['风格：',style_tags],['主角身份：',status_tgs],['主角形象：',figure_tgs],['故事流派：',story_tgs],['故事元素：',story_ele_tgs]]);
// 文档加载时把标签创建出来

$(function(){
	for (var [key,value] of tags) {
		let label_ele = $('<label>'+key+'</label>');
		$('.tags-box').append(label_ele);
		// $('.tags-box').append($('<div class="tags-item"></div>'));
		value.forEach(function(item){
			let input_ele = $('<input type="checkbox" name="tags" value="'+item+'"><span>'+item+'</span>');
			$('.tags-box').append(input_ele);
			// $('.tags-item').append(input_ele);
		});
		$('.tags-box').append($('<br><br>'));
	}
});

// window.onload = function(){

// }
// 文档加载时把累计收入计算出来
$('td.book-income').each(function(index,val){
	total_money += parseFloat($(val).text());
});
$('.economy p span i').first().text(total_money);

$('.uinfo-left-top a').each(function(){
	$(this).click(function(){
		$('.uinfo-left a').each(function(){
			$(this).attr("class","");
		});
		$(this).attr("class","uinfo-active");

	});
});

// 更改用户头像信息
// avatar.change(function(){
// 	imageFile = $(this)[0].files[0];
// 	console.log(imageFile);
// 	url = URL.createObjectURL(imageFile);//能获取图片的url
// 	$(this).prev().prev().attr('src',url);
// 	formdata.append("file",imageFile);
// 	// console.log(formdata.get("file"));
// 	$.ajax({
// 		type:'POST',
// 		url:'/edit_avatar/',
// 		// data:{csrfmiddlewaretoken:'{{ csrf_token}}',user_avatar:formdata},
// 		// header:{"X-CSRFToken": $.cookie('csrftoken')},
// 		data:{user_avatar:formdata},
// 		// contentType:false,
// 		processData:false,
// 		success:function(result){
// 			console.log(result.useravatar);
// 			$('.uinfo-avatar img').attr("src",result.useravatar);
// 		},
// 		error:function(result){
// 			console.log("失败");
// 		}

// 	});
// })
// // 更改用户名
// var username = $('.uinfo-level input');
// username.change(function(){
// 	userid = $(this).attr('data-userid');
// 	$.ajax({
// 		type:'POST',
// 		url:'/user/'+userid+'/',
// 		data:{username:username.val()},
// 		// contentType:false,
// 		success:function(result){
// 			username.val() = result.username;
// 		}
// 	});
// })
// 管理书籍中显示章节
$('.chapter-list .link').click(function(){
	$(this).nextAll().last().toggleClass("display");
})

// 管理书籍中发布书籍
$('.chapter-opretion').on('click','.chapter-pub',function(){
	wordsnum = $(this).parent().prev().children().last().attr('data-word-num');
	pub_a = $(this);
	chapterid = pub_a.parent().parent().attr('data-chapter');
	if (wordsnum>=1000) {
		$.get('/mycreate/'+bookid+'/pub_chapter/'+chapterid+'/',function(){
			pub_a.after('<a>已发布</a>');
			pub_a.remove();
		});
	}
});


// 修改章节内容
$('.chapter-opretion .update-chapter').click(function(){
	if ($(this).parent().next().attr('class') == 'chapter-content left-part display') {
		$(this).parent().next().toggleClass('display');
	}
	$('.chapter-content').attr('contenteditable','true');
	// $(this).parent().html('<button>确定</botton>');
	$(this).parent().css('display','none');
	$(this).parent().after('<div class="chapter-opretion"><button>确定</botton></div>');

})
// 禁止章节的复制
$('.chapter-content').on('paste',function(){
	return false;
});
// 点击修改后，给生成的确认按钮添加点击事件，
$('.chapter-item').on('click','.chapter-opretion button',function(){
	opretion_btn = $(this);
	chaptertext = $(this).parent().next().html();
	chaptertext = chaptertext.replace(/<div>/g,'');
	chaptertext = chaptertext.replace(/<\/div>/g,'<br/>');
	chapterid = opretion_btn.parent().parent().attr('data-chapter');
	$.post('/mycreate/'+bookid+'/edit_chapter/'+chapterid+'/',{chaptercontent:chaptertext},function(result){
		if (!opretion_btn.parent().prev().children().first().attr('class')) {
			opretion_btn.parent().prev().children().first().attr('class','chapter-pub');
			opretion_btn.parent().prev().children().first().text('发布')
		}
		opretion_btn.parent().prev().prev().children().last().attr('data-word-num',result.wordnum);
		opretion_btn.parent().next().attr('contenteditable','false');
		opretion_btn.parent().prev().css('display','block');
		opretion_btn.parent().next().html(chaptertext);
		opretion_btn.parent().prev().prev().children().last().text(result.wordnum+'字');
		opretion_btn.parent().remove();
	})
})
//使textarea根据输入内容的高度自适应
jQuery.fn.extend({
	autoHeight: function(){
		return this.each(function(){
			var $this = jQuery(this);
			if( !$this.attr('_initAdjustHeight') ){
				$this.attr('_initAdjustHeight', $this.outerHeight());
			}
			_adjustH(this).on('input', function(){
				_adjustH(this);
			});
		});
		function _adjustH(elem){
			var $obj = jQuery(elem);
			return $obj.css({height: $obj.attr('_initAdjustHeight'), 'overflow-y': 'hidden'})
					.height( elem.scrollHeight );
		}
	}
	});
// 使用
$(function(){
	$('.chapter-text').autoHeight();
});
// 上传图片即时显示在界面上
$('.bookcover-box input').change(function(){
	url = URL.createObjectURL($(this)[0].files[0]);//能获取图片的url
	$(this).prev().attr('src',url);
});
$('.uinfo-avatar input').change(function(){
	url = URL.createObjectURL($(this)[0].files[0]);//能获取图片的url
	$(this).prev().attr('src',url);
});
// 创建书籍，书名不能为空
$('.create-book .bookname-input').change(function(){
	flag = false;
	str = $(this).val();
	if (str.replace(/[ ]/g,'') =='') {
		flag = false;
		if ($(this).next().length == 0) {
			$(this).after('<i>*不能为空<i>');
		}
		else{
			$(this).next().text('*不能为空');
		}
	}
	else{
		flag = true;
		$(this).val(str.replace(/[ ]/g,''));
		$(this).next().text('');
	}
	if (flag) {
		$('.create-book button').removeAttr('disabled');
	}
});
// 书籍发布和下架
$('.book-detail-info').on('click','.book-pub',function(){
	pub_btn = $(this);
	$.get('/mycreate/'+bookid+'/bookpub/',function(result){
		if (result.book_status) {
			pub_btn.text('下架');
		}
		else{
			pub_btn.text('发布');
		}
	})
});
// 作者自定义价格
$('.price-select').change(function(){
	let word_num = parseInt($(this).parent().prev().children().last().attr('data-word-num')/1000);
	let price = $(this).val()*word_num
	chapterid = $(this).parent().parent().attr('data-chapter');
	$.post('/'+chapterid + '/makeprice/',{price:price});
});
// 作者完结书籍
$('.end-btn').click(function(){
	end_btn = $(this);
	$.get('/'+bookid+'/endbook/',function(){
		$('.book-state-text').text('已完结');
		end_btn.prev().remove();
		end_btn.remove();
	})
});
// 检测用户输入的金额是否大于已有金额
$('.economy-form input').change(function(){
	cash = parseFloat($('#cash').text());
	if ($(this).val()>cash) {
		$(this).next().attr('disabled','true');
		$('.economy-form p').text('*不能超过总金额');
	}
	else{
		if ($(this).next().attr('disabled')) {
			$(this).next().removeAttr('disabled');
			$('.economy-form p').text('');
		}
	}
});
//删除评论
$('.del').click(function(){
	let commentid = $(this).attr('data-commentid')
	delc_btn = $(this)
	$.get('/delcomment/'+commentid+'/',function(result){
		if (result.delcomment) {
			delc_btn.parent().parent().remove();
		}
	});
});
// 发布公告
$('.pub-notice').click(function(){
	$('.notice-text').toggleClass('display');
	let notice = $('.notice-text textarea').val();
	if (notice) {
		$.post('/mycreate/'+bookid+'/pubnotice/',{notice:notice},function(){
			showmessage('发布成功');
		});
	}
});