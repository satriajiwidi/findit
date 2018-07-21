$('document').ready(function () {
    var url = window.location.href;
    url = url.split('/')
    var len_url = url.length;
    console.log(url, len_url);

    if (url[3] == 'attractions' && url[4] !== "") {
        // $('div.sidebar div ul li:nth-child(1)').removeClass('active');
        // $('div.sidebar div ul li:nth-child(2)').addClass('active');
        $('nav div a h3').text('Beranda');
        $('nav div a.navbar-brand').attr('href', '/attractions');
    } else if (url[3] == '') {
        $('nav div a').empty();
        $('#logo-navbar').empty();
        $('nav div a.navbar-brand').append('<h3 id="place">Kupantau</h3>');
    } else if (url[3] == 'attractions' && url[4] == "") {
        // $('div.sidebar div ul li:nth-child(1)').addClass('active');
        // $('div.sidebar div ul li:nth-child(2)').removeClass('active');
        $('nav div a h3').text('Beranda');
        $('nav div a.navbar-brand').attr('href', '/');
    }
});