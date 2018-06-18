$(document).ready(function() {
    var carousel = $('.carousel').carousel();
    var screensaver = $("#screensaver");
    screensaver.click(function() {
        $(this).hide();
        screensaver.carousel(0);
        screensaver.carousel('pause');

        setTimeout(function() {
            screensaver.carousel(0);
            screensaver.show();
        }, 30000)
    });
});