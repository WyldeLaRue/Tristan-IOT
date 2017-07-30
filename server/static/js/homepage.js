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

function setPatternFromElement(element){
	return function() { 
		var pattern = element.value;
		$.get("/api/lights/patterns/" + pattern, function( data ) {
			console.log("Sent " + pattern);
		});
	}
}

function setPatternCarriageReturn(element) {
	return function(event){
	    if (event.which == 13 || event.keyCode == 13) {
	    	pattern = element.value;
	        $.get("/api/lights/patterns/" + pattern);
	        return false;
	    }
	    return true;
	}
};

function setAttribute(element, attribute) {
	return function () {
		var value = element.value;
		document.getElementById(attribute + "SliderValue").textContent = value;
		$.post("/api/lights/setAttribute", {value: value, attribute: attribute});
	};
}

function getRequest(path) {
	return function() {
		$.get(path);
	}
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
	bindPatternById('strobe');
	bindPatternById('rainbowStrobe');
	bindPatternById('TBD');
	var patternInput = document.getElementById('arbitraryPatternInput');
	document.getElementById("arbitraryPatternSubmit").onclick = setPatternFromElement(patternInput);
	patternInput.onkeypress = setPatternCarriageReturn(patternInput);

	document.getElementById("clearPatterns").onclick = getRequest("/api/lights/clearPatterns");
	document.getElementById("debug").onclick = getRequest("/debug");

	var speed = document.getElementById('speedSlider');
	speed.oninput = setAttribute(speed, "speed");
	var brightness = document.getElementById('brightnessSlider');
	brightness.oninput = setAttribute(brightness, "brightness");
	var generic1 = document.getElementById('generic1');
	var generic2 = document.getElementById('generic2');
	var generic3 = document.getElementById('generic3');
	generic1.oninput = setAttribute(generic1, "generic1");
	generic2.oninput = setAttribute(generic2, "generic2");
	generic3.oninput = setAttribute(generic3, "generic3");


	for (i = 1; i <= 5; i++) {
		document.getElementById('outlet-' + i + '-on').onclick = toggleOutlet(i, 'ON');
		document.getElementById('outlet-' + i + '-off').onclick = toggleOutlet(i, 'OFF');
	}
}

bindEvents();

$(document).ready(function() {
	console.log('test');
});