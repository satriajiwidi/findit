$('document').ready(function () {
    $.get('http://localhost:5000/apis/images_index', function (json_data) {
        $data = JSON.parse(json_data);
        console.log($data);

        // $("div.font-icon-detail").each(function (index) {
        //     console.log(index + ": " + $(this).attr('src', $images[index]));
        // });

        $('div.row div.font-icon-detail img').each(function (index) {
            $(this).attr('src', $data['file_paths'][index]);
        });

        $('div.row div.font-icon-detail p').each(function (index) {
            $(this).text($data['attracts'][index]);
        });
    });
});