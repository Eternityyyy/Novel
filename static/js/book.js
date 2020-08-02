var collectstatus;
var bookid = $('.book-collect img').attr('data-bookid');
// 收藏
collectstatus = $('.book-collect .collect-img').attr('data-collect-status');
if (collectstatus =='True') {
	$('.book-mess .addrack').css('background','#e9e9e9');
	$('.book-mess .addrack').text('移除书架');
}
// 评论
$('.comment-btn').click(function(){
	$(this).parent().next().toggleClass('display');
	if ($(this).parent().next().attr('class') == 'comment-textarea') {
		$(this).text('收起评论');

	}
	else{
		$(this).text('我要评论');
	}
});
// 加入书架
function addRack(data){
	$('.book-mess .addrack').text('加入书架');
	$('.book-mess .addrack').css('background','#f05952');
	$('.book-collect .collect-img').attr({'src':'/static/img/un-collect.png','data-collect-status':'False'});
	$('.book-collect i').text(data.collect_num);
}
// 移除书架
function removeRack(data){
	$('.book-mess .addrack').css('background','#e9e9e9');
	$('.book-mess .addrack').text('移除书架');
	$('.book-collect .collect-img').attr({'src':'/static/img/collect.png','data-collect-status':'True'});
	$('.book-collect i').text(data.collect_num);
}
// 收藏
function Collect(ele){
	collectstatus = $('.book-collect .collect-img').attr('data-collect-status');
	if (collectstatus == 'True') {
		$.get('/book/'+bookid+'/uncollect/',function(data){
			addRack(data);
		});
	}
	else{
		$.get('/book/'+bookid+'/collect/',function(data){
			removeRack(data);
		});	
	}
}

// 对收藏添加点击
$('.book-collect .collect-img').click(function(){
	Collect($(this));

})
$('.book-mess .addrack').click(function(){
	Collect($(this));

});
// 送推荐票
$('.fans-ticket button').click(function(){
	$.get('/book/'+bookid+'/recommend/',function(data){
		if (data.recommend) {
			$('.fans-ticket span i').text(data.recommend);
		}
		else{
			// alert('你没有推荐票');
			showmessage('你没有推荐票');
		}
	})
});
// 送礼物
$('.gif-item').click(function(){
	$.get('/book/'+bookid+'/gif/',function(data){
		if (data.gif) {
			$('.fansmove p i').text(data.gif);
		}
		else{
			// alert('金币不够哟，快去充值');
			showmessage('金币不够哟，快去充值');
		}
	});
});

