var preTimeout = null;
var realTimeout = null;
var counterInterval = null;
var counterTimeout = 30;

function resetTimeouts(e) {
    clearTimeout(preTimeout);
    clearTimeout(realTimeout);
    clearInterval(counterInterval);
    counterTimeout = 30;
    $("#timeoutPopup").hide();

    preTimeout = setTimeout(function () {
        $("#timeoutPopup").show();
        counterInterval = setInterval(function () {
            if (counterTimeout > 0) {
                counterTimeout -= 1;
            }
            $('#timeoutPopup span').text(counterTimeout);
        }, 1000);
        realTimeout = setTimeout(function () {
            var xhr = new XMLHttpRequest();

            xhr.open('POST', '/');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function() {
                if (xhr.status === 200) {}
            };
            xhr.send(encodeURI('action=timeout'));

        }, 30*1000);
    }, 60*1000);
}
document.onclick = resetTimeouts;
resetTimeouts();
