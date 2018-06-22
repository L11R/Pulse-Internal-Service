'use strict';

$(document).ready(function () {
    var carousel = $('.carousel').carousel();
    var screensaver = $("#screensaver");
    screensaver.click(function () {
        $(this).hide();
        screensaver.carousel(0);
        screensaver.carousel('pause');

        setTimeout(function () {
            screensaver.carousel(0);
            screensaver.show();
        }, 30000);
    });
});
//# sourceMappingURL=data:application/json;charset=utf8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNjcmVlbnNhdmVyLmpzIl0sIm5hbWVzIjpbIiQiLCJkb2N1bWVudCIsInJlYWR5IiwiY2Fyb3VzZWwiLCJzY3JlZW5zYXZlciIsImNsaWNrIiwiaGlkZSIsInNldFRpbWVvdXQiLCJzaG93Il0sIm1hcHBpbmdzIjoiOztBQUFBQSxFQUFFQyxRQUFGLEVBQVlDLEtBQVosQ0FBa0IsWUFBVztBQUN6QixRQUFJQyxXQUFXSCxFQUFFLFdBQUYsRUFBZUcsUUFBZixFQUFmO0FBQ0EsUUFBSUMsY0FBY0osRUFBRSxjQUFGLENBQWxCO0FBQ0FJLGdCQUFZQyxLQUFaLENBQWtCLFlBQVc7QUFDekJMLFVBQUUsSUFBRixFQUFRTSxJQUFSO0FBQ0FGLG9CQUFZRCxRQUFaLENBQXFCLENBQXJCO0FBQ0FDLG9CQUFZRCxRQUFaLENBQXFCLE9BQXJCOztBQUVBSSxtQkFBVyxZQUFXO0FBQ2xCSCx3QkFBWUQsUUFBWixDQUFxQixDQUFyQjtBQUNBQyx3QkFBWUksSUFBWjtBQUNILFNBSEQsRUFHRyxLQUhIO0FBSUgsS0FURDtBQVVILENBYkQiLCJmaWxlIjoic2NyZWVuc2F2ZXIuanMiLCJzb3VyY2VzQ29udGVudCI6WyIkKGRvY3VtZW50KS5yZWFkeShmdW5jdGlvbigpIHtcbiAgICB2YXIgY2Fyb3VzZWwgPSAkKCcuY2Fyb3VzZWwnKS5jYXJvdXNlbCgpO1xuICAgIHZhciBzY3JlZW5zYXZlciA9ICQoXCIjc2NyZWVuc2F2ZXJcIik7XG4gICAgc2NyZWVuc2F2ZXIuY2xpY2soZnVuY3Rpb24oKSB7XG4gICAgICAgICQodGhpcykuaGlkZSgpO1xuICAgICAgICBzY3JlZW5zYXZlci5jYXJvdXNlbCgwKTtcbiAgICAgICAgc2NyZWVuc2F2ZXIuY2Fyb3VzZWwoJ3BhdXNlJyk7XG5cbiAgICAgICAgc2V0VGltZW91dChmdW5jdGlvbigpIHtcbiAgICAgICAgICAgIHNjcmVlbnNhdmVyLmNhcm91c2VsKDApO1xuICAgICAgICAgICAgc2NyZWVuc2F2ZXIuc2hvdygpO1xuICAgICAgICB9LCAzMDAwMClcbiAgICB9KTtcbn0pOyJdfQ==
