pstn_app["on_message"] = function(obj){
      console.log("GOT MESSAGE INSIDE: " + obj);
      if ( obj.cell_closed ){
        document.getElementById("cell_open_state").innerHTML = "Ячейка закрыта";
        document.getElementById("actions_block").style.visibility = 'visible';

      }
};
console.log(pstn_app);
