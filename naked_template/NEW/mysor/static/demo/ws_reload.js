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
    obj = JSON.parse(event.data)
    console.log(obj);

    if ( obj.do_reload === true) {
        document.location.reload(true);
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
