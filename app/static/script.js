//var url = "http://192.168.29.198:50000";
//var url = "http://192.168.29.202:50000";
var url = "http://localhost:50000";

var scrWidth, scrHeight;
var imgWidth = 800;
var imgHeight;

var scrImage = document.getElementById("scrImage");
var leftButton = document.getElementById("leftButton");
var rightButton = document.getElementById("rightButton");
var textInput = document.getElementById("textInput");
var inputButton = document.getElementById("inputButton");

document.body.onload = function() {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url+"/init");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onreadystatechange = function() {
	   if (xhr.readyState === XMLHttpRequest.DONE) {
		  data = JSON.parse(xhr.responseText);
		  scrWidth = data.width;
		  scrHeight = data.height;
		  imgHeight = parseInt(imgWidth / scrWidth * scrHeight);
		  scrImage.style.width = ""+imgWidth+"px";
		  scrImage.style.height = ""+imgHeight+"px";
		  scrImage.src = "data:image/jpg;base64," + data.image;
	   }};
	
	var data = {};
	data.type = "screen";

	xhr.send(JSON.stringify(data));	
}

scrImage.onclick = function(ev) {
	console.log(ev);
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url+"/move");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	
	var data = {};
	data.x = ev.offsetX;
	data.y = ev.offsetY;
	data.width = imgWidth;
	data.height = imgHeight;

	xhr.send(JSON.stringify(data));	
}

leftButton.onclick = function() {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url+"/left");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onreadystatechange = function() {
	   if (xhr.readyState === XMLHttpRequest.DONE) {
		  data = JSON.parse(xhr.responseText);
		  scrImage.src = "data:image/jpg;base64," + data.image;
	   }};
	
	var data = {};
	data.type = "screen";

	xhr.send(JSON.stringify(data));	
	
}

rightButton.onclick = function() {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url+"/right");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onreadystatechange = function() {
	   if (xhr.readyState === XMLHttpRequest.DONE) {
		  data = JSON.parse(xhr.responseText);
		  scrImage.src = "data:image/jpg;base64," + data.image;
	   }};
	
	var data = {};
	data.type = "screen";

	xhr.send(JSON.stringify(data));	
	
}

inputButton.onclick = function() {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url+"/input");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onreadystatechange = function() {
	   if (xhr.readyState === XMLHttpRequest.DONE) {
		  data = JSON.parse(xhr.responseText);
		  scrImage.src = "data:image/jpg;base64," + data.image;
	   }};
	
	var data = {};
	data.input = textInput.value;

	xhr.send(JSON.stringify(data));	
	
}
