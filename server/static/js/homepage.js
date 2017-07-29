/*====================================
   Factory Functions for Ajax Calls  
====================================*/
function setPattern(pattern) {
	return function () {
		$.get("/api/lights/patterns/" + pattern, function( data ) {
			console.log("Sent " + pattern);
		});
	}
}

function setAttribute(element, attribute) {
	return function () {
		var value = element.value;
		document.getElementById(attribute + "SliderValue").textContent = value;
		$.post("/api/lights/setAttribute", {value: value, attribute: attribute});
	};
}

function toggleOutlet(outletId, state) {
	return function () {
		$.post("/api/outlets/toggle", {outletId: outletId, state: state});
	}
}


function start() {
	$.get("/start");
}


function helloFactory(string) {
	return function() {
		alert(string);
	};
}


/*====================================
   		  Utility Functions 
====================================*/

function bindPatternById(id) {
	document.getElementById(id).onclick = setPattern(id);
}



function bindEvents() {
	bindPatternById('rainbow');
	bindPatternById('rainbowCycle');
	bindPatternById('debug');

	document.getElementById('START').onclick =  function(){start();};

	var speed = document.getElementById('speedSlider');
	speed.oninput = setAttribute(speed, "speed");
	var brightness = document.getElementById('brightnessSlider')
	brightness.oninput = setAttribute(brightness, "brightness");

	for (i = 1; i <= 5; i++) {
		document.getElementById('outlet-' + i + '-on').onclick = toggleOutlet(i, 'ON');
		document.getElementById('outlet-' + i + '-off').onclick = toggleOutlet(i, 'OFF');
	}
}

bindEvents();

$(document).ready(function() {
	console.log('test');
});