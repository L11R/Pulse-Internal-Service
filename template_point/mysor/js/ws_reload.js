
function WebSocketClient(){
    this.number = 0;	// Message number
    this.autoReconnectInterval = 1000;	// ms
}
WebSocketClient.prototype.open = function(url){
    this.url = url;
    this.instance = new WebSocket(this.url);
    this.instance.onopen = () => {
        this.onopen();
    };
    this.instance.onmessage = (data,flags)=> {
        this.number++;
        this.onmessage(data, flags, this.number);
    };
    this.instance.onclose = (e)=>{
        switch (e){
            case 1000:	// CLOSE_NORMAL
                console.log("WebSocket: closed");
                break;
            default:	// Abnormal closure
                this.reconnect(e);
                break;
        }
        this.onclose(e);
    };
    this.instance.onerror = (e)=>{
        switch (e.code){
            case 'ECONNREFUSED':
                this.reconnect(e);
                break;
            default:
                this.onerror(e);
                break;
        }
    };
};
WebSocketClient.prototype.send = function(data,option){
    try{
        this.instance.send(data,option);
    }catch (e){
        this.instance.emit('error',e);
    }
};
WebSocketClient.prototype.reconnect = function(e){
    console.log(`WebSocketClient: retry in ${this.autoReconnectInterval}ms`,e);
    var that = this;
    setTimeout(function(){
        console.log("WebSocketClient: reconnecting...");
        that.open(that.url);
    },this.autoReconnectInterval);
};
WebSocketClient.prototype.onopen = function(e){	console.log("WebSocketClient: open",arguments);	};
WebSocketClient.prototype.onmessage = function(data,flags,number){	console.log("WebSocketClient: message",arguments);	};
WebSocketClient.prototype.onerror = function(e){	console.log("WebSocketClient: error",arguments);	};
WebSocketClient.prototype.onclose = function(e){	console.log("WebSocketClient: closed",arguments);	};


var sock = new WebSocketClient();
sock.open('ws://' + window.location.host + '/ui/ws');
sock.onmessage = function(event) {
    console.log(event);
    var obj = JSON.parse(event.data);
    console.log(obj);

    if ( obj.do_reload === true) {
        document.location.reload(true);
    } else if (obj.cell_event) {
        var cell_id = obj.cell_event.cell_id;
        var $cell = $("#cell-"+cell_id);
        // Reset classes. TODO: find more generic way
        $cell.removeClass("opened");
        $cell.removeClass("dirty");
        $cell.removeClass("operational");
        $cell.removeClass("broken");
        $cell.removeClass("blocked");
        $cell.addClass(obj.cell_event.cell_state);
        if (obj.cell_event.is_open && obj.cell_event.cell_state == "operational") {
            $cell.addClass("opened");
        }
        $cell.find('span').text(obj.cell_event.cell_state);
    }
};
