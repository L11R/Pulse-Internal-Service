// Replace with kiosk self signal through redis.


function send_check(){

    console.log("BEFORE SEND check expired")
    var formData = new FormData();

    formData.append("action", "courier_start_check_expired");

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function()
    {
        if(xmlHttp.readyState == 4 && xmlHttp.status == 200)
        {
    //        alert(xmlHttp.responseText);
        }
    }
    xmlHttp.open("post", "/");
    xmlHttp.send(formData);


    console.log("sent: " + formData);
};


try{
  var sock = new WebSocket('ws://' + window.location.host + '/ui/ws');
}
catch(err){
  var sock = new WebSocket('wss://' + window.location.host + '/ui/ws');
}


sock.onopen = function(){
  console.log('Connection to server started');
  send_check();

}

// income message handler
sock.onmessage = function(event) {
    var obj = JSON.parse(event.data);
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
