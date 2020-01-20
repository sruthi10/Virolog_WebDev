
function drawChart(pvalue = 0.5) {
    var ctx = document.getElementById("myChart").getContext('2d');
    $.getJSON( "/getcleavagesitesdata/" + pvalue, function(jsondata){
        var cleavagelabels = jsondata['cleavagemappinglabels'];
        var cleavagesitevaluesvirus = jsondata['cleavagesitevaluesvirus'];
        var cleavagesitevalueshuman = jsondata['cleavagesitevalueshuman'];
        var cleavagesitevaluesmouse = jsondata['cleavagesitevaluesmouse'];

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: cleavagelabels,
                datasets: [{
                    label: 'Virus',
                    data: cleavagesitevaluesvirus,
                    backgroundColor: 'rgba(254, 101, 1, 1)',
                    borderColor: 'rgba(254, 101, 1, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Human',
                    data: cleavagesitevalueshuman,
                    backgroundColor: 'rgba(98, 0, 164, 1)',
                    borderColor: 'rgba(98, 0, 164, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Mouse',
                    data: cleavagesitevaluesmouse,
                    backgroundColor: 'rgba(15, 173, 0, 1)',
                    borderColor: 'rgba(15, 173, 0, 1)',
                    borderWidth: 1
                }]
            },
            options: {
              scales: {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: 'Number of Genes having this Cleavage Count'
                }
            }],
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Position of Cleavage Site'
                }
            }]
        },
        pan: {
                // Boolean to enable panning
                enabled: true,

                // Panning directions. Remove the appropriate direction to disable
                // Eg. 'y' would only allow panning in the y direction
                mode: 'xy'
            },

                // Container for zoom options
        zoom: {
                // Boolean to enable zooming
                enabled: true,

                // Zooming directions. Remove the appropriate direction to disable
                // Eg. 'y' would only allow zooming in the y direction
                mode: 'y',
            }
        },
        });
    });
}

