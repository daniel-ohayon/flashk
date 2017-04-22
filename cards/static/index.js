var SLICE_COLORS = {
    'new': 'purple',
    'good': 'green',
    'average': 'orange',
    'poor': 'red'
};

$(document).ready(function() {

    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(getDataAndDrawChart);

    function getDataAndDrawChart() {
        $.get('stats/', function(data) {
            drawPieChart(data['current-data']);
            drawStackedBarChart(data['past-data']);
            $('#review-div').show();  // display review button only once the graphs are displayed
        });
    }

    function drawPieChart(stats) {

        var data = google.visualization.arrayToDataTable(stats, false);

        // build an object mapping data table row index to slice label
        var indexToLabel = {};
        $.each(stats, function(index, row) {
            if (index === 0) { return; }
            indexToLabel[index-1] = row[0].toLowerCase();
        });

        var sliceOptions = {};
        $.each(indexToLabel, function(index, label) {
            sliceOptions[index] = SLICE_COLORS[label];
        });

        var options = {
            'width':250,
            'height':300,
            'slices': sliceOptions,
            'pieHole': 0.4,
            'legend': {'position': 'top'},
            'chartArea': {'width': '100%'}
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart-div'));
        google.visualization.events.addListener(chart, 'click', clickHandler);

        function clickHandler(event) {
            // if one of the slices is clicked, go to the corresponding list view
            var targetID = event.targetID;
            if (targetID.startsWith("slice#")) {
                var sliceIndex = parseInt(targetID.split('#')[1]);
                var label = indexToLabel[sliceIndex];
                document.location.href = 'list/' + label + '/';
            }

        }

        chart.draw(data, options);
    }

    function drawStackedBarChart(stats) {
        var data = google.visualization.arrayToDataTable(stats, false);
        var chart = new google.visualization.ColumnChart(document.getElementById('barchart-div'));
        chart.draw(data, {
            'width': 400,
            'height': 250,
            'legend': {'position': 'top'},
            'chartArea': {'width': '100%'},
            isStacked: true,
            'series': { // TODO remove hardcoding
                0: {'color': 'red'},
                1: {'color': 'orange'},
                2: {'color': 'green'}
            }
        });
    }

});
