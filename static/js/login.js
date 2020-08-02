createCode();
code_box.querySelector(".code-img").onclick = function(){
		createCode();
	}
// window.onload= function(){
// }
code_box.querySelector("input").onchange =function(){
	validateCode();
	if (codeflag) {
		document.querySelector(".register-login").querySelector("button").attributes.removeNamedItem("disabled");
		console.log(document.querySelector(".register-login").querySelector("button").attributes.length);
	}
	else{
		let disable = document.createAttribute("disabled");
		document.querySelector(".register-login").querySelector("button").attributes.setNamedItem(disable);		
		console.log(document.querySelector(".register-login").querySelector("button").attributes.length);
	}
}