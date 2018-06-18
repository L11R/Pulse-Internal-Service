// todo: use instead of ws_reload.js

var pstn_app = {"sock": null, "on_message": null};

try{
  var sock = new WebSocket('ws://' + window.location.host + '/ui/ws');
}
catch(err){
  var sock = new WebSocket('wss://' + window.location.host + '/ui/ws');
}


sock.onopen = function(){
  console.log('Connection to server started')
}

// income message handler
sock.onmessage = function(event) {
    var obj = JSON.parse(event.data);
    console.log(obj);

    if ( obj.do_reload === true) {
        document.location.reload(true);
    } else {
        // if( pstn_app["on_message"] !== null){
            pstn_app["on_message"](obj)
        //}
    }

};

sock.onclose = function(event){
  if(event.wasClean){
      console.log('Clean connection end')
  }else{
      console.log('Connection broken')
  }
};

sock.onerror = function(error){
  console.log(error);
}

pstn_app["sock"] = sock;
