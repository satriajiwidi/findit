$('document').ready(function () {
    var url = window.location.href;
    var query = url.split('?q=')[1];

    url = 'http://localhost:5000/apis/images';
    if (query !== undefined) {
        url += '/?q=' + query;
    }

    console.log(url);

    $.get(url, function (json_data) {
        $data = JSON.parse(json_data);
        console.log($data);

        // $("div.font-icon-detail").each(function (index) {
        //     console.log(index + ": " + $(this).attr('src', $images[index]));
        // });

        var len_data = $data['attracts'].length;

        if (len_data > 0) {
            for (i = 0; i < len_data; i++) {
                string_html = '<div class="font-icon-list col-3">'
                string_html += '<a href="' + '/attractions/' + $data['file_paths'][i].split('/')[2] + '">'
                string_html += '<div class="font-icon-detail">'
                string_html += '<img width="100%" height="200" src="../' + $data['file_paths'][i] + '">'
                string_html += '<p>' + $data['attracts'][i] + '</p>'
                string_html += '</div></a></div>'

                $('div.attractions').append(string_html);
            }
        } else {
            $('div.attractions').append('<p>Tidak ditemukan</p>');
        }

    });
});