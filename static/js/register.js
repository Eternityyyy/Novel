// var register_state = {{ register_state|safe }};
var nameflag = false,pasflag = false,newpasflag = false;
var user_box = document.querySelector(".username");
var pas_box = document.querySelector(".pas");
var new_pas_box = document.querySelector(".new_pas");

// window.onload = function(){
createCode();

// }

function testUser(){
	let error_message = "";
	let inputtext = user_box.querySelector("input").value;
	if (inputtext.length<=0) {
		error_message ="用户名不能为空";
	}
	else if (inputtext.length>=50) {
		error_message = "用户名太长了不好记"
	}
	nameflag = isError(error_message,user_box,nameflag);

}
function testPas(){
	let error_message = "";
	let inputtext = pas_box.querySelector("input").value;
	if (inputtext.length<=0) {
		error_message = "密码不能为空";
	}
	else if (inputtext.length<=6) {
		error_message = "密码太简单";
	}
	else if (inputtext.length>=120) {
		error_message = "密码不合法";
	}
	pasflag = isError(error_message,pas_box,pasflag);
}
function testNew_pas(){
	let error_message = "";
	let pasinput = pas_box.querySelector("input").value;
	let newinput = new_pas_box.querySelector("input").value;
	if (pasinput != newinput) {
		error_message = "两次输入密码不一样";
	}
	newpasflag = isError(error_message,new_pas_box,newpasflag);
}

user_box.querySelector("input").onchange =function(){
	testUser();
	isDisabled();
}
pas_box.querySelector("input").onchange =function(){
	testPas();
	isDisabled();
}
new_pas_box.querySelector("input").onchange = function(){
	testNew_pas();
	isDisabled();
}
code_box.querySelector("input").onchange =function(){
	validateCode();
	isDisabled();
}
function isDisabled(){
	if (nameflag&&pasflag&&newpasflag&&codeflag) {
		document.querySelector(".register").querySelector("button").attributes.removeNamedItem("disabled");
		console.log(document.querySelector(".register").querySelector("button").attributes.length);
	}
	else{
		let disable = document.createAttribute("disabled");
		document.querySelector(".register").querySelector("button").attributes.setNamedItem(disable);		
		console.log(document.querySelector(".register").querySelector("button").attributes.length);
	}
}
code_box.querySelector(".code-img").onclick = function(){
		createCode();
	}