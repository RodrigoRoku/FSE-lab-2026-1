function deactivateAll(){
	//var buttons = document.getElementsByTagName('button');
	var buttons = document.querySelectorAll('button');
  console.log(buttons.length)
  for(let i = 0; i < buttons.length; i++){
		buttons[i].classList.remove("on")
  }
}

function activate(sender){
	if(sender == null)
		return;
	sender.classList.add("on");
}

function handle(sender, action, value){
	deactivateAll();
	activate(sender);
	submit(action, value);
}

function submit(action, value){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", window.location.href, true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify({
		'action' : action,
		'value' :  value,
	}));
}