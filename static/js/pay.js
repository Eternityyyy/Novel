
var spans = document.querySelector('.pay-box').querySelectorAll('span');

spans.forEach(function(span){
	span.addEventListener("click",function(){
		document.querySelector('#money-input').value = parseFloat(this.querySelector('i').innerHTML)/100;
	});
});

