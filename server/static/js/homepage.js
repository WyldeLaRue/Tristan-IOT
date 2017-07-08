function setPattern(pattern) {
    $.get( "/api/patterns/" + pattern, function( data ) {
      console.log("Sent " + pattern);
    });
}
// var rainbowButton = document.getElementById("rainbow");
// rainbowButton.addEventListener("onclick", 
//                                function() {setPattern("rainbow");}
//                                );


// var rainbowCycleButton = document.getElementById("rainbowCycle");
// rainbowCycleButton.addEventListener("onclick", 
//                                function() {setPattern("rainbowCycle");}
//                                );

function toggleOutlet(outletId, state) {
    $.post( "/api/outlets/toggle", {outletId: outletId, state: state});
}


function start() {
    $.get("/start");
}
