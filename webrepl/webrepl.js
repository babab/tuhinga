(function() {

    $('#full-width').click(function() {
        $('.col-lg-6').removeClass('col-lg-6').addClass('col-lg-12')
    });
    $('#side-by-side').click(function() {
        $('.col-lg-12').removeClass('col-lg-12').addClass('col-lg-6')
    });

    $('#src').keyup(function() {
        $('#dest').text("And it's gone");
    });

})();
