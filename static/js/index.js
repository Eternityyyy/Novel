var Rollbtn,RollUl,Rollbtn_lis,Rollactive;

	// 设置定时器让首页的滚动图片滚动起来
setInterval(function(){
	RollUl = document.querySelector(".roll-ul");
	Rollbtn = document.querySelector(".roll-btn");
	Rollbtn_lis = Rollbtn.querySelectorAll("li");
	Rollactive = document.querySelector(".li-active");

	RollUl.insertBefore(RollUl.lastElementChild,RollUl.firstElementChild);
	for (var i = 0; i < Rollbtn_lis.length; i++) {
		Rollbtn_lis[i].className = "";
	}
	if (Rollactive.nextElementSibling) {
		Rollactive.nextElementSibling.className = "li-active";
	}
	else
		Rollbtn_lis[0].className = "li-active";
},3000);
