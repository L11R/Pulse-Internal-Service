
// Set up the canvas
var canvas = document.getElementById("sig-canvas");
var ctx = canvas.getContext("2d");
ctx.strokeStyle = "#222222";
ctx.lineWith = 2;

// Set up mouse events for drawing
var drawing = false;
var mousePos = { x:0, y:0 };
var lastPos = mousePos;
canvas.addEventListener("touchstart", function (e) {
    drawing = true;
    lastPos = getMousePos(canvas, e);
}, false);
canvas.addEventListener("touchend", function (e) {
    drawing = false;
}, false);
canvas.addEventListener("touchmove", function (e) {
    mousePos = getMousePos(canvas, e);
}, false);
canvas.addEventListener("mousedown", function (e) {
    drawing = true;
    lastPos = getMousePos(canvas, e);
}, false);
canvas.addEventListener("mouseup", function (e) {
    drawing = false;
}, false);
canvas.addEventListener("mousemove", function (e) {
    mousePos = getMousePos(canvas, e);
}, false);

// Get the position of the mouse relative to the canvas
function getMousePos(canvasDom, mouseEvent) {
    var rect = canvasDom.getBoundingClientRect();
    if (mouseEvent.touches != undefined) {
        mouseEvent = mouseEvent.touches[0];
    }
    return {
        x: mouseEvent.clientX - rect.left,
        y: mouseEvent.clientY - rect.top
    };
}

// Get a regular interval for drawing to the screen
window.requestAnimFrame = (function (callback) {
    return window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimaitonFrame ||
        function (callback) {
            window.setTimeout(callback, 1000/60);
        };
})();


// Draw to the canvas
function renderCanvas() {
    if (drawing && mousePos.x != 0 && mousePos.y != 0) {
        ctx.moveTo(lastPos.x, lastPos.y);
        ctx.lineTo(mousePos.x, mousePos.y);
        ctx.stroke();
        lastPos = mousePos;
    }
}

// Allow for animation
(function drawLoop () {
    requestAnimFrame(drawLoop);
    renderCanvas();
})();


function push_data(data){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function()
    {
        if(xhr.readyState == 4 && xhr.status == 200)
        {
            console.log("got response: " +  xhr.responseText);
            document.location.reload(true);
        }
    }
    xhr.open("post", "/");
    xhr.send(data);
}

function isCanvasBlank() {
    var blank = document.createElement('canvas');
    blank.width = canvas.width;
    blank.height = canvas.height;

    return canvas.toDataURL() == blank.toDataURL();
}


function inform_kiosk(print_bill) {

    if (isCanvasBlank()) {
        return;
    }

    var dataURL = canvas.toDataURL("image/png");
    console.log("Sign: " + dataURL);

    var formData = new FormData();
    formData.append("action", "send_signature");
    formData.append("print_bill", print_bill);
    formData.append("signature_bitmap", dataURL);

    push_data(formData);

}


document.getElementById("no_print_bill").addEventListener("click", function(e) {
    inform_kiosk("no");
});

document.getElementById("print_bill").addEventListener("click", function(e) {
    inform_kiosk("yes");
});
