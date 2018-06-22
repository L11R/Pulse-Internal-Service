window.ondragstart = function() { return false; };

function perform_post(path, params, method) {
    // using: recipe from https://stackoverflow.com/questions/133925/javascript-post-request-like-a-form-submit


    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}

$(document).ready(function () {
    $(".to_idle").click(function (e) {
        perform_post("/", { "action": "timeout"});
    });
});
