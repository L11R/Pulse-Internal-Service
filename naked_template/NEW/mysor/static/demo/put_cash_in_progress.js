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

    document.getElementById("registered_cash").innerHTML = obj.registered_cash;
    document.getElementById("last_banknote").innerHTML = obj.last_banknote;

    if (obj.registered_cash >= 100.0) {
        document.getElementById("open_small_section").style.display = 'block';
    }

    if (obj.registered_cash >= 200.0) {
        document.getElementById("open_medium_section").style.display = 'block';
    }

    if (obj.registered_cash >= 300.0) {
        document.getElementById("open_big_section").style.display = 'block';
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
