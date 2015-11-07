/*
Admin Gateway javascript
*/

// Admin Gateway menu loading
$(document).ready(function() {
    $('#AdminGtwyMenu').load('https://admin-dev.telekom.ee/static/admin-gtwy-nav.html');
    $('#AdminGtwyMenu').hide();

    $("#AdminGtwyNavButton").click(function(){
        $("#AdminGtwyMenu").toggle();
        $("#NavButtonGlyph").toggleClass('glyphicon glyphicon-menu-down').toggleClass('glyphicon glyphicon-menu-up');
    });
});