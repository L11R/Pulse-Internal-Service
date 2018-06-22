"use strict";

// todo: use instead of ws_reload.js

var pstn_app = { "sock": null, "on_message": null };

try {
    var sock = new WebSocket('ws://' + window.location.host + '/ui/ws');
} catch (err) {
    var sock = new WebSocket('wss://' + window.location.host + '/ui/ws');
}

sock.onopen = function () {
    console.log('Connection to server started');
};

// income message handler
sock.onmessage = function (event) {
    var obj = JSON.parse(event.data);
    console.log(obj);

    if (obj.do_reload === true) {
        document.location.reload(true);
    } else {
        // if( pstn_app["on_message"] !== null){
        pstn_app["on_message"](obj
        //}
        );
    }
};

sock.onclose = function (event) {
    if (event.wasClean) {
        console.log('Clean connection end');
    } else {
        console.log('Connection broken');
    }
};

sock.onerror = function (error) {
    console.log(error);
};

pstn_app["sock"] = sock;
//# sourceMappingURL=data:application/json;charset=utf8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbImFwcC5qcyJdLCJuYW1lcyI6WyJwc3RuX2FwcCIsInNvY2siLCJXZWJTb2NrZXQiLCJ3aW5kb3ciLCJsb2NhdGlvbiIsImhvc3QiLCJlcnIiLCJvbm9wZW4iLCJjb25zb2xlIiwibG9nIiwib25tZXNzYWdlIiwiZXZlbnQiLCJvYmoiLCJKU09OIiwicGFyc2UiLCJkYXRhIiwiZG9fcmVsb2FkIiwiZG9jdW1lbnQiLCJyZWxvYWQiLCJvbmNsb3NlIiwid2FzQ2xlYW4iLCJvbmVycm9yIiwiZXJyb3IiXSwibWFwcGluZ3MiOiI7O0FBQUE7O0FBRUEsSUFBSUEsV0FBVyxFQUFDLFFBQVEsSUFBVCxFQUFlLGNBQWMsSUFBN0IsRUFBZjs7QUFFQSxJQUFHO0FBQ0QsUUFBSUMsT0FBTyxJQUFJQyxTQUFKLENBQWMsVUFBVUMsT0FBT0MsUUFBUCxDQUFnQkMsSUFBMUIsR0FBaUMsUUFBL0MsQ0FBWDtBQUNELENBRkQsQ0FHQSxPQUFNQyxHQUFOLEVBQVU7QUFDUixRQUFJTCxPQUFPLElBQUlDLFNBQUosQ0FBYyxXQUFXQyxPQUFPQyxRQUFQLENBQWdCQyxJQUEzQixHQUFrQyxRQUFoRCxDQUFYO0FBQ0Q7O0FBR0RKLEtBQUtNLE1BQUwsR0FBYyxZQUFVO0FBQ3RCQyxZQUFRQyxHQUFSLENBQVksOEJBQVo7QUFDRCxDQUZEOztBQUlBO0FBQ0FSLEtBQUtTLFNBQUwsR0FBaUIsVUFBU0MsS0FBVCxFQUFnQjtBQUM3QixRQUFJQyxNQUFNQyxLQUFLQyxLQUFMLENBQVdILE1BQU1JLElBQWpCLENBQVY7QUFDQVAsWUFBUUMsR0FBUixDQUFZRyxHQUFaOztBQUVBLFFBQUtBLElBQUlJLFNBQUosS0FBa0IsSUFBdkIsRUFBNkI7QUFDekJDLGlCQUFTYixRQUFULENBQWtCYyxNQUFsQixDQUF5QixJQUF6QjtBQUNILEtBRkQsTUFFTztBQUNIO0FBQ0lsQixpQkFBUyxZQUFULEVBQXVCWTtBQUMzQjtBQURJO0FBRVA7QUFFSixDQVpEOztBQWNBWCxLQUFLa0IsT0FBTCxHQUFlLFVBQVNSLEtBQVQsRUFBZTtBQUM1QixRQUFHQSxNQUFNUyxRQUFULEVBQWtCO0FBQ2RaLGdCQUFRQyxHQUFSLENBQVksc0JBQVo7QUFDSCxLQUZELE1BRUs7QUFDREQsZ0JBQVFDLEdBQVIsQ0FBWSxtQkFBWjtBQUNIO0FBQ0YsQ0FORDs7QUFRQVIsS0FBS29CLE9BQUwsR0FBZSxVQUFTQyxLQUFULEVBQWU7QUFDNUJkLFlBQVFDLEdBQVIsQ0FBWWEsS0FBWjtBQUNELENBRkQ7O0FBSUF0QixTQUFTLE1BQVQsSUFBbUJDLElBQW5CIiwiZmlsZSI6ImFwcC5qcyIsInNvdXJjZXNDb250ZW50IjpbIi8vIHRvZG86IHVzZSBpbnN0ZWFkIG9mIHdzX3JlbG9hZC5qc1xuXG52YXIgcHN0bl9hcHAgPSB7XCJzb2NrXCI6IG51bGwsIFwib25fbWVzc2FnZVwiOiBudWxsfTtcblxudHJ5e1xuICB2YXIgc29jayA9IG5ldyBXZWJTb2NrZXQoJ3dzOi8vJyArIHdpbmRvdy5sb2NhdGlvbi5ob3N0ICsgJy91aS93cycpO1xufVxuY2F0Y2goZXJyKXtcbiAgdmFyIHNvY2sgPSBuZXcgV2ViU29ja2V0KCd3c3M6Ly8nICsgd2luZG93LmxvY2F0aW9uLmhvc3QgKyAnL3VpL3dzJyk7XG59XG5cblxuc29jay5vbm9wZW4gPSBmdW5jdGlvbigpe1xuICBjb25zb2xlLmxvZygnQ29ubmVjdGlvbiB0byBzZXJ2ZXIgc3RhcnRlZCcpXG59XG5cbi8vIGluY29tZSBtZXNzYWdlIGhhbmRsZXJcbnNvY2sub25tZXNzYWdlID0gZnVuY3Rpb24oZXZlbnQpIHtcbiAgICB2YXIgb2JqID0gSlNPTi5wYXJzZShldmVudC5kYXRhKTtcbiAgICBjb25zb2xlLmxvZyhvYmopO1xuXG4gICAgaWYgKCBvYmouZG9fcmVsb2FkID09PSB0cnVlKSB7XG4gICAgICAgIGRvY3VtZW50LmxvY2F0aW9uLnJlbG9hZCh0cnVlKTtcbiAgICB9IGVsc2Uge1xuICAgICAgICAvLyBpZiggcHN0bl9hcHBbXCJvbl9tZXNzYWdlXCJdICE9PSBudWxsKXtcbiAgICAgICAgICAgIHBzdG5fYXBwW1wib25fbWVzc2FnZVwiXShvYmopXG4gICAgICAgIC8vfVxuICAgIH1cblxufTtcblxuc29jay5vbmNsb3NlID0gZnVuY3Rpb24oZXZlbnQpe1xuICBpZihldmVudC53YXNDbGVhbil7XG4gICAgICBjb25zb2xlLmxvZygnQ2xlYW4gY29ubmVjdGlvbiBlbmQnKVxuICB9ZWxzZXtcbiAgICAgIGNvbnNvbGUubG9nKCdDb25uZWN0aW9uIGJyb2tlbicpXG4gIH1cbn07XG5cbnNvY2sub25lcnJvciA9IGZ1bmN0aW9uKGVycm9yKXtcbiAgY29uc29sZS5sb2coZXJyb3IpO1xufVxuXG5wc3RuX2FwcFtcInNvY2tcIl0gPSBzb2NrOyJdfQ==
