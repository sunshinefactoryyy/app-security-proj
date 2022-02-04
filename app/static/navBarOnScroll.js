
jQuery(function ($) {
    var $navbar = $('.fixed-top');
    $(window).scroll(function (event) {
        var $current = $(this).scrollTop();
        if ($current > $(window).height()) {
            $navbar.addClass('changeColor');
        } else {
            $navbar.removeClass('changeColor');
        }
    });
});