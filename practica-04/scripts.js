var marquee = null
function deactivateAll(){
	//var buttons = document.getElementsByTagName('button');
	var buttons = document.querySelectorAll('button');
  console.log(marquee)
	if(typeof(marquee) != "undefined" && marquee !== null){
		clearInterval(marquee)
		marquee = null
	}
  for(let i = 0; i < buttons.length; i++){
		buttons[i].classList.remove("on")
  }
}

function activate(sender){
	if(sender == null)
		return;
	if(sender.id == "mleft"){
		marqueeleft();
	}else if(sender.id == "mright"){
		marqueeRight();
	}else if(sender.id == "pingpong"){
		pingPong();
	}
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

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function marqueeRight(){
	var buttons = document.querySelectorAll('[id=led]');
	var i = 0;
	marquee =  setInterval(() => {
		//console.log("Mensaje cada 0.5 seg")
		buttons[i].classList.add("on");
		console.log(i);
		if(i > 0){
			buttons[i - 1].classList.remove("on");
		}else{
			buttons[buttons.length - 1].classList.remove("on");
		}
		i = i + 1 ;
		if(i >= buttons.length){
			i = 0;
		}
	}, 1000)

}

function marqueeleft(){
	var buttons = document.querySelectorAll('[id=led]');
	var i = buttons.length - 1;
	marquee =  setInterval(() => {
		buttons[i].classList.add("on");
		console.log(i);
		if(i < buttons.length - 1){
			buttons[i + 1].classList.remove("on");
		}else{
			buttons[0].classList.remove("on");
		}
		i-- ;
		if(i < 0){
			i = buttons.length - 1;
		}
	}, 1000)

}

function pingPong(){
	var buttons = document.querySelectorAll('[id=led]');
	var i = 0;
	var inc = 1;
	marquee =  setInterval(() => {
		
		if(i >= buttons.length || i < 0){
			i = i - inc
			inc = inc * (-1)
		}else{
			if(i !== 0)
				buttons[i-inc].classList.remove("on");
			else
				buttons[i].classList.remove("on");
		}
		buttons[i].classList.add("on");
		console.log(i);
		i = i + inc;

	}, 1000)

}

//animateMarquee();
