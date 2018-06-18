"use strict";

window.ondragstart = function () {
    return false;
};

function perform_post(path, params, method) {
    // using: recipe from https://stackoverflow.com/questions/133925/javascript-post-request-like-a-form-submit


    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for (var key in params) {
        if (params.hasOwnProperty(key)) {
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
        perform_post("/", { "action": "timeout" });
    });
});
//# sourceMappingURL=data:application/json;charset=utf8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbImNvbW1vbi5qcyJdLCJuYW1lcyI6WyJ3aW5kb3ciLCJvbmRyYWdzdGFydCIsInBlcmZvcm1fcG9zdCIsInBhdGgiLCJwYXJhbXMiLCJtZXRob2QiLCJmb3JtIiwiZG9jdW1lbnQiLCJjcmVhdGVFbGVtZW50Iiwic2V0QXR0cmlidXRlIiwia2V5IiwiaGFzT3duUHJvcGVydHkiLCJoaWRkZW5GaWVsZCIsImFwcGVuZENoaWxkIiwiYm9keSIsInN1Ym1pdCIsIiQiLCJyZWFkeSIsImNsaWNrIiwiZSJdLCJtYXBwaW5ncyI6Ijs7QUFBQUEsT0FBT0MsV0FBUCxHQUFxQixZQUFXO0FBQUUsV0FBTyxLQUFQO0FBQWUsQ0FBakQ7O0FBRUEsU0FBU0MsWUFBVCxDQUFzQkMsSUFBdEIsRUFBNEJDLE1BQTVCLEVBQW9DQyxNQUFwQyxFQUE0QztBQUN4Qzs7O0FBR0FBLGFBQVNBLFVBQVUsTUFBbkIsQ0FKd0MsQ0FJYjs7QUFFM0I7QUFDQTtBQUNBLFFBQUlDLE9BQU9DLFNBQVNDLGFBQVQsQ0FBdUIsTUFBdkIsQ0FBWDtBQUNBRixTQUFLRyxZQUFMLENBQWtCLFFBQWxCLEVBQTRCSixNQUE1QjtBQUNBQyxTQUFLRyxZQUFMLENBQWtCLFFBQWxCLEVBQTRCTixJQUE1Qjs7QUFFQSxTQUFJLElBQUlPLEdBQVIsSUFBZU4sTUFBZixFQUF1QjtBQUNuQixZQUFHQSxPQUFPTyxjQUFQLENBQXNCRCxHQUF0QixDQUFILEVBQStCO0FBQzNCLGdCQUFJRSxjQUFjTCxTQUFTQyxhQUFULENBQXVCLE9BQXZCLENBQWxCO0FBQ0FJLHdCQUFZSCxZQUFaLENBQXlCLE1BQXpCLEVBQWlDLFFBQWpDO0FBQ0FHLHdCQUFZSCxZQUFaLENBQXlCLE1BQXpCLEVBQWlDQyxHQUFqQztBQUNBRSx3QkFBWUgsWUFBWixDQUF5QixPQUF6QixFQUFrQ0wsT0FBT00sR0FBUCxDQUFsQzs7QUFFQUosaUJBQUtPLFdBQUwsQ0FBaUJELFdBQWpCO0FBQ0g7QUFDSjs7QUFFREwsYUFBU08sSUFBVCxDQUFjRCxXQUFkLENBQTBCUCxJQUExQjtBQUNBQSxTQUFLUyxNQUFMO0FBQ0g7O0FBRURDLEVBQUVULFFBQUYsRUFBWVUsS0FBWixDQUFrQixZQUFZO0FBQzFCRCxNQUFFLFVBQUYsRUFBY0UsS0FBZCxDQUFvQixVQUFVQyxDQUFWLEVBQWE7QUFDN0JqQixxQkFBYSxHQUFiLEVBQWtCLEVBQUUsVUFBVSxTQUFaLEVBQWxCO0FBQ0gsS0FGRDtBQUdILENBSkQiLCJmaWxlIjoiY29tbW9uLmpzIiwic291cmNlc0NvbnRlbnQiOlsid2luZG93Lm9uZHJhZ3N0YXJ0ID0gZnVuY3Rpb24oKSB7IHJldHVybiBmYWxzZTsgfTtcblxuZnVuY3Rpb24gcGVyZm9ybV9wb3N0KHBhdGgsIHBhcmFtcywgbWV0aG9kKSB7XG4gICAgLy8gdXNpbmc6IHJlY2lwZSBmcm9tIGh0dHBzOi8vc3RhY2tvdmVyZmxvdy5jb20vcXVlc3Rpb25zLzEzMzkyNS9qYXZhc2NyaXB0LXBvc3QtcmVxdWVzdC1saWtlLWEtZm9ybS1zdWJtaXRcblxuXG4gICAgbWV0aG9kID0gbWV0aG9kIHx8IFwicG9zdFwiOyAvLyBTZXQgbWV0aG9kIHRvIHBvc3QgYnkgZGVmYXVsdCBpZiBub3Qgc3BlY2lmaWVkLlxuXG4gICAgLy8gVGhlIHJlc3Qgb2YgdGhpcyBjb2RlIGFzc3VtZXMgeW91IGFyZSBub3QgdXNpbmcgYSBsaWJyYXJ5LlxuICAgIC8vIEl0IGNhbiBiZSBtYWRlIGxlc3Mgd29yZHkgaWYgeW91IHVzZSBvbmUuXG4gICAgdmFyIGZvcm0gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiZm9ybVwiKTtcbiAgICBmb3JtLnNldEF0dHJpYnV0ZShcIm1ldGhvZFwiLCBtZXRob2QpO1xuICAgIGZvcm0uc2V0QXR0cmlidXRlKFwiYWN0aW9uXCIsIHBhdGgpO1xuXG4gICAgZm9yKHZhciBrZXkgaW4gcGFyYW1zKSB7XG4gICAgICAgIGlmKHBhcmFtcy5oYXNPd25Qcm9wZXJ0eShrZXkpKSB7XG4gICAgICAgICAgICB2YXIgaGlkZGVuRmllbGQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KFwiaW5wdXRcIik7XG4gICAgICAgICAgICBoaWRkZW5GaWVsZC5zZXRBdHRyaWJ1dGUoXCJ0eXBlXCIsIFwiaGlkZGVuXCIpO1xuICAgICAgICAgICAgaGlkZGVuRmllbGQuc2V0QXR0cmlidXRlKFwibmFtZVwiLCBrZXkpO1xuICAgICAgICAgICAgaGlkZGVuRmllbGQuc2V0QXR0cmlidXRlKFwidmFsdWVcIiwgcGFyYW1zW2tleV0pO1xuXG4gICAgICAgICAgICBmb3JtLmFwcGVuZENoaWxkKGhpZGRlbkZpZWxkKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoZm9ybSk7XG4gICAgZm9ybS5zdWJtaXQoKTtcbn1cblxuJChkb2N1bWVudCkucmVhZHkoZnVuY3Rpb24gKCkge1xuICAgICQoXCIudG9faWRsZVwiKS5jbGljayhmdW5jdGlvbiAoZSkge1xuICAgICAgICBwZXJmb3JtX3Bvc3QoXCIvXCIsIHsgXCJhY3Rpb25cIjogXCJ0aW1lb3V0XCJ9KTtcbiAgICB9KTtcbn0pOyJdfQ==
