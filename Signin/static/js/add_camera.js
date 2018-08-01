/*Added_module_camera Init*/
var SendRequestAddCamera = function () {
	var settings = {
  "async": true,
  "crossDomain": true,
  "url": "../add_camera/",
  "method": "POST",
  "headers": {
    "authorization": $.cookie('token'),
    "cache-control": "no-cache"
  },
  "processData": false,
  "contentType": false,
  "mimeType": "multipart/form-data",
  "data": JSON.stringify({"url": $('#url_address').val()})
	};
	console.log('Hhhhhhhui');
	$.ajax(settings).done(function (response) {
		console.log(response);
	});
};

$( document ).ready(function() {
	"use strict";

	$("#added_camera").on('click', function () {
	    SendRequestAddCamera();
	});
});