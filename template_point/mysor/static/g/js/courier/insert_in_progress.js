"use strict";

pstn_app["on_message"] = function (obj) {
  console.log("GOT MESSAGE INSIDE: " + obj);
  if (obj.cell_closed) {
    document.getElementById("cell_open_state").innerHTML = "Ячейка закрыта";
    document.getElementById("actions_block").style.display = 'block';
  }
};
console.log(pstn_app);
//# sourceMappingURL=data:application/json;charset=utf8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbImNvdXJpZXIvaW5zZXJ0X2luX3Byb2dyZXNzLmpzIl0sIm5hbWVzIjpbInBzdG5fYXBwIiwib2JqIiwiY29uc29sZSIsImxvZyIsImNlbGxfY2xvc2VkIiwiZG9jdW1lbnQiLCJnZXRFbGVtZW50QnlJZCIsImlubmVySFRNTCIsInN0eWxlIiwiZGlzcGxheSJdLCJtYXBwaW5ncyI6Ijs7QUFBQUEsU0FBUyxZQUFULElBQXlCLFVBQVNDLEdBQVQsRUFBYTtBQUNoQ0MsVUFBUUMsR0FBUixDQUFZLHlCQUF5QkYsR0FBckM7QUFDQSxNQUFLQSxJQUFJRyxXQUFULEVBQXNCO0FBQ3BCQyxhQUFTQyxjQUFULENBQXdCLGlCQUF4QixFQUEyQ0MsU0FBM0MsR0FBdUQsZ0JBQXZEO0FBQ0FGLGFBQVNDLGNBQVQsQ0FBd0IsZUFBeEIsRUFBeUNFLEtBQXpDLENBQStDQyxPQUEvQyxHQUF5RCxPQUF6RDtBQUNEO0FBQ04sQ0FORDtBQU9BUCxRQUFRQyxHQUFSLENBQVlILFFBQVoiLCJmaWxlIjoiY291cmllci9pbnNlcnRfaW5fcHJvZ3Jlc3MuanMiLCJzb3VyY2VzQ29udGVudCI6WyJwc3RuX2FwcFtcIm9uX21lc3NhZ2VcIl0gPSBmdW5jdGlvbihvYmope1xuICAgICAgY29uc29sZS5sb2coXCJHT1QgTUVTU0FHRSBJTlNJREU6IFwiICsgb2JqKTtcbiAgICAgIGlmICggb2JqLmNlbGxfY2xvc2VkICl7XG4gICAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKFwiY2VsbF9vcGVuX3N0YXRlXCIpLmlubmVySFRNTCA9IFwi0K/Rh9C10LnQutCwINC30LDQutGA0YvRgtCwXCI7XG4gICAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKFwiYWN0aW9uc19ibG9ja1wiKS5zdHlsZS5kaXNwbGF5ID0gJ2Jsb2NrJztcbiAgICAgIH1cbn07XG5jb25zb2xlLmxvZyhwc3RuX2FwcCk7Il19
