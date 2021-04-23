// alert('If you see this alert, then your custom JavaScript script has run!')



$(document).ready(function(){
    $("#menu").on("click","a", function (event) {
        event.preventDefault();
        var id  = $(this).attr('href'),
            top = $(id).offset().top;
        $('body,html').animate({scrollTop: top-45}, 1000);
    });
});