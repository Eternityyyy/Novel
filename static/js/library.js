var pre_url,pre_url_arr,add_url;
var that;

// window.onload = function(){
// 	pre_url = window.location.search;
// 	if (pre_url.length>1) {
// 		pre_url_arr = pre_url.split('?')[1].split('&');
// 		console.log(pre_url_arr);
// 		let data_conditions = $('[data-condition]');
// 		for(let i in data_conditions){
// 			for (let j in pre_url_arr){
// 				if (pre_url_arr[j] == $(data_conditions[i]).attr('data-condition')) {
// 					$(data_conditions[i]).addClass('condition-active');
// 				}
// 			}
// 		}
// 	}
// }


//处理url不重叠
function Dealurl(streg){
	pre_url = window.location.search;
	add_url = that.attr('data-condition');
	if (add_url.length>1){
		if (pre_url.length<1) {
			that.attr('href',pre_url+'?'+add_url);
		}
		else{
			add_url_item = add_url.split('=')[0]+'=\\d*';
			let reg = new RegExp(add_url_item);
			if (reg.test(pre_url)) {
				that.attr('href',pre_url.replace(reg,add_url));
			}
			else{
				that.attr('href',pre_url+'&'+add_url);
			}
		}	
	}
	else{
		let spacereg = new RegExp('&*'+streg+'=\\d*');
		that.attr('href',pre_url.replace(spacereg,''));
	}

}

$('.library-category a').on('click',function(){
	that = $(this);
	Dealurl('category');
});
$('.condition-order a').on('click',function(){
	that = $(this);
	Dealurl('order');
});
$('.condition-state a').on('click',function(){
	that = $(this);
	Dealurl('state');
});
$('.pagination a').on('click',function(){
	that = $(this);
	Dealurl('page');
});


