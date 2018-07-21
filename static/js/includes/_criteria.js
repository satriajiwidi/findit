$('document').ready(function () {
    function toTitleCase(str) {
        return str.replace(/\w\S*/g, function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    function cetak_pie($series, $labels, $indices, $komentars) {
        $labelsCaps = []
        for (i = 0; i < $labels.length; i++) {
            $labelsCaps.push(toTitleCase($labels[i]));
        }

        var data = {
            datasets: [{
                data: $series,
                backgroundColor: [
                    "rgba(255, 0, 0, .5)",
                    "rgba(255, 100, 100, .5)",
                    "rgba(255, 200, 200, .5)",
                    "rgba(100, 255, 100, .5)",
                    "rgba(100, 255, 255, .5)",
                    "rgba(100, 100, 255, .5)",
                    "rgba(100, 0, 255, .5)",
                    "rgba(0, 0, 255, .5)"
                ],
                borderColor: [
                    "rgba(255, 0, 0, .5)",
                    "rgba(255, 100, 100, .5)",
                    "rgba(255, 200, 200, .5)",
                    "rgba(100, 255, 100, .5)",
                    "rgba(100, 255, 255, .5)",
                    "rgba(100, 100, 255, .5)",
                    "rgba(100, 0, 255, .5)",
                    "rgba(0, 0, 255, .5)"
                ]
            }],
            labels: $labelsCaps
        };

        var canvas = document.getElementById("pie-chart");
        var ctx = canvas.getContext("2d");
        var myNewChart = new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                hover: {
                    onHover: function (e, el) {
                        $("#pie-chart").css("cursor", el[0] ? "pointer" : "default");
                    }
                }
            }
        });

        canvas.onclick = function (evt) {
            var activePoints = myNewChart.getElementsAtEvent(evt);

            $("#myModal div.modal-body").empty();

            if (activePoints[0]) {
                var chartData = activePoints[0]['_chart'].config.data;
                var idx = activePoints[0]['_index'];
                var label = chartData.labels[idx].toLowerCase();

                for (i = 0; i < $indices[label].length; i++) {
                    comment = $komentars[$indices[label][i]];
                    $("#myModal div.modal-body").append('<p>' + comment + '</p>');
                }
                
                $('#myModal h5').text(toTitleCase(label));

                $('#myModal').modal('show');
            }
        };
    }

    var id_attract = window.location.href;
    id_attract = id_attract.split('/')[4];
    console.log(id_attract);

    var $counter = $.get('http://localhost:5000/apis/attractions/'+id_attract, function (json_data) {
        $data = JSON.parse(json_data);

        $('h3#place').text($data['place']);
        
        $aspeks = $data['aspeks'];
        $komentars = $data['komentars'];
        $counter = $data['counter'];

        console.log($data);

        // demo.initDashboardPageCharts($counter);

        $labels = []
        for (var key in $counter) {
            $labels.push(key);
        }

        $series = []
        for (var key in $counter) {
            $series.push($counter[key]);
        }

        function getAllIndexes(arr, val) {
            var indexes = [], i = -1;
            while ((i = arr.indexOf(val, i + 1)) != -1) {
                indexes.push(i);
            }
            return indexes;
        }

        var $indices = {};
        for (var index in $labels) {
            $indices[$labels[index]] = getAllIndexes($aspeks, $labels[index])
        }

        console.log('index', $indices);
        var isNoSaran = jQuery.isEmptyObject($indices);

        if (isNoSaran) {
            $('.pie-chart-div').append('<p>Belum ada respon aspek negatif yang ditemukan</p>');
        } else {
            cetak_pie($series, $labels, $indices, $komentars);
        }

    });

    $.get('http://localhost:5000/apis/attractions/' + id_attract + '/suggestions', function (json_data) {
        $data = JSON.parse(json_data);
        console.log($data);

        $('table.table td.saran').each(function (index) {
            $(this).text($data['suggestions'][index]);
        });
    });

    $.get('http://localhost:5000/apis/attractions/' + id_attract + '/sentiment', function (json_data) {
        $data = JSON.parse(json_data);
        console.log($data);
        
        for (i = 0; i < $data['preds'].length; i++) {
            text = $data['texts'][i];
            pred = $data['preds'][i];
            if (pred == 1) {
                pred = 'positif';
            } else {
                pred = 'negatif';
            }
            $('tbody.sentiment').append(
                "<tr><td class='saran'>" + text + "</td><td class='saran " + pred + "'>" + pred + "</td></tr>"
            );
        }
    });
});