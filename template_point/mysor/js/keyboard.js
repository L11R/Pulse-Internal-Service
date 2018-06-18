var currentField = document.getElementById("id_login");

if (!currentField) {
    currentField = document.getElementById("id_order_id");
}

if (document.getElementById("id_passwd")) {
    document.getElementById("id_passwd").onclick = function (e) {
        currentField = e.target;
    };
}

if (document.getElementById("id_login")) {
    document.getElementById("id_login").onclick = function (e) {
        currentField = e.target;
    };
}

document.querySelector(".keyboard").onclick=function (e) {
    if (e.target.className.indexOf("letter") >= 0) {
        if (e.target.className.indexOf("backspace") >= 0) {
            if (currentField.value.length) {
                currentField.value = currentField.value.slice(0, -1);
            }
        } else if (e.target.className.indexOf("shifted") >= 0) {
            allToLower()
        } else if (e.target.className.indexOf("shift") >= 0) {
            allToUpper()
        } else if (currentField.value.length < currentField.maxLength || currentField.maxLength < 0) {
            currentField.value = currentField.value + e.target.value;
        }
        e.target.blur();
    }
};

function allToUpper() {
    var letters = document.getElementsByClassName("letter");
    for (var i = 0; i < letters.length; i++) {
        var target = letters[i];
        if (target.className.indexOf("letter") >= 0) {
            if (target.className.indexOf("shift") >= 0) {
                target.className = target.className.replace(/(?:^|\s)shift(?!\S)/g, "shifted")
            } else {
                target.value = target.value.toUpperCase()
            }
        }
    }

}

function allToLower() {
    var letters = document.getElementsByClassName("letter");
    for (var i = 0; i < letters.length; i++) {
        var target = letters[i];
        if (target.className.indexOf("letter") >= 0) {
            if (target.className.indexOf("shifted") >= 0) {
                target.className = target.className.replace(/(?:^|\s)shifted(?!\S)/g, "shift")
            } else {
                target.value = target.value.toLowerCase()
            }
        }
    }

}