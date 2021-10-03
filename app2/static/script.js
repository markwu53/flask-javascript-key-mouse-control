//var url = "http://192.168.29.202:50000";
//var url = "http://localhost:50000";
var url = "http://192.168.29.198:50000";

var scrWidth, scrHeight;
var imgWidth = 800;
var imgHeight;

var scrImage = document.getElementById("scrImage");
var leftButton = document.getElementById("leftButton");
var rightButton = document.getElementById("rightButton");
var textInput = document.getElementById("textInput");
var inputButton = document.getElementById("inputButton");
var actionTable = document.getElementById("actionTable");
var saveActions = document.getElementById("saveActions");
var clearActions = document.getElementById("clearActions");
var runActions = document.getElementById("runActions");
var actionTitle = document.getElementById("actionTitle");

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

clearActions.onclick = function() {
	while (actionTable.firstChild) {
		actionTable.removeChild(actionTable.firstChild);
	}
	actionTitle.value = "";
}

runActions.onclick = function() {
	if (actionTitle.value == "") {
		alert("please enter a title");
		return;
	}
	
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url+"/run");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	
	xhr.onreadystatechange = function() {
		   if (xhr.readyState === XMLHttpRequest.DONE) {
				//var data = JSON.parse(xhr.responseText);
		   }};

	var data = {};
	data.title = actionTitle.value;
	xhr.send(JSON.stringify(data));	
}

saveActions.onclick = function() {
	var actions = [];
	var es = actionTable.getElementsByClassName("actionMessage");
	const length = es.length;
	if (length == 0) {
		alert("nothing to save");
		return;
	}
	for (var i = 0; i < length; i ++) {
		actions.push(es[i].textContent);
	}

	if (actionTitle.value == "") {
		alert("please enter a title");
		return;
	}
	
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url+"/save");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	
	xhr.onreadystatechange = function() {
		   if (xhr.readyState === XMLHttpRequest.DONE) {
				//var data = JSON.parse(xhr.responseText);
		   }};

	var data = {};
	data.title = actionTitle.value;
	data.actions = actions;
	xhr.send(JSON.stringify(data));	
}

function addAction(message) {
	var tr, td, button, div;
	tr = actionTable.insertRow();
	td = tr.insertCell();
	div = document.createElement("div");
	div.textContent = message;
	div.className = "actionMessage";
	td.appendChild(div);
	td = tr.insertCell();
	button = document.createElement("button");
	button.className = "actionDelete";
	button.innerHTML = "X";
	td.appendChild(button);
	button.onclick = function() {
		tr.remove();
	}
}

scrImage.onclick = function(ev) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", url+"/move");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	
	xhr.onreadystatechange = function() {
		   if (xhr.readyState === XMLHttpRequest.DONE) {
				//var data = JSON.parse(xhr.responseText);
		   }};

	var data = {};
	data.x = ev.offsetX;
	data.y = ev.offsetY;
	data.width = imgWidth;
	data.height = imgHeight;

	xhr.send(JSON.stringify(data));	
	
	var x = parseInt(data.x/data.width * 100000)/100000;
	var y = parseInt(data.y/data.height * 100000)/100000;
	addAction("mouse,move,"+x+","+y);
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
	data.type = "mouse";
	data.action = "left";

	xhr.send(JSON.stringify(data));	
	
	addAction("mouse,left");
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
	
	addAction("mouse,right");
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
	
	addAction("key,"+data.input);
}
