$(document).ready(function() {

    $("#move_to_main_two, #move_to_main_three").on("click", function (e) {
        e.preventDefault();
        var $findElement = $(this).attr('id').split('_')[3];
        var $element = new Array('main', $findElement, 'catch').join('_');
        $('html, body').animate({
            scrollTop: $("#"+ $element).offset().top - 45
        }, 500);
    });

    $("#en, #pl").on("click", function(e) {
        e.preventDefault();
        Cookies.set("lang", $(this).attr('id'), {path: "/", expires: 30});
        location.reload()
    });

});