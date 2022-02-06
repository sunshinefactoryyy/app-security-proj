
jQuery(function ($) {
    var $navBar = $('.fixed-top');
    $(window).scroll(function (event) {
        var $current = $(this).scrollTop();
        if ($current > $(window).height()) {
            $navBar.addClass('changeColor');
        } else {
            $navBar.removeClass('changeColor');
        }
    });
});