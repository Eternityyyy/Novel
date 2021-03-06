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