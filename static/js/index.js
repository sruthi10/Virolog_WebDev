var currentChart;
var filteredViralTax = ["''"];
var familyList = ["''"];
var realm = '';

function createFamilyOptions() {
    $.getJSON( "/getFamilies/" + realm, function(families){
        console.log(families['values']);
        var select = document.getElementById("family");
        select.innerHTML = '';

        for (const val of families['values']) {
            var option = document.createElement("option");
            option.value = val;
            option.text = val;
            select.appendChild(option);
        }
    });
}

function addFamily(family) {
    if (currentChart.data.labels.includes(family)) {
        return
    }
    familyList.push(`'`+family+`'`);
    $.getJSON( "/getFamilyCount/" + family, function(jsonData){
        currentChart.data.labels.push(family);
        currentChart.data.datasets.forEach((dataset) => {
            dataset.data.push(jsonData['count']);
        });
        currentChart.update();
        buildHtmlTable('#taxTable');
    });
}

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

function drawChartProbability(pvalueMin = 0.5, pvalueMax = 1.0) {
    var ctx = document.getElementById("myChart").getContext('2d');
    $.getJSON( "/getPresequenceProbabilityData/" + pvalueMin + "/" + pvalueMax, function(jsondata){
        var probabilityvaluesvirus = jsondata["probabilityvaluesvirus"];
        var probabilityvalueshuman = jsondata["probabilityvalueshuman"];
        var probabilityvaluesmouse = jsondata["probabilityvaluesmouse"];
        var probabilitylabels = jsondata["probabilitymappinglabels"];
        if (currentChart) {
            currentChart.destroy();
        }
        currentChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: probabilitylabels,
                datasets: [{
                    label: 'Virus',
                    data: probabilityvaluesvirus,
                    borderColor: 'rgba(254, 101, 1, 1)',
                },
                           {
                               label: 'Human',
                               data: probabilityvalueshuman,
                               borderColor: 'rgba(98, 0, 164, 1)',
                               fill: false
                           },
                           {
                               label: 'Mouse',
                               data: probabilityvaluesmouse,
                               borderColor: 'rgba(15, 173, 0, 1)',
                               fill: false
                           }]
            },
            options: {
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Number of Genes'
                        }
                    }],
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Probability'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(2); //truncate
                            }
                        }
                    }]
                },
            },
        });
    });
    $("#probability-play").hide();
}

function getColors(numberOfColours) {
    var colorArray = [
        "#e6194b",
        "#3cb44b",
        "#ffe119",
        "#0082c8",
        "#f58231",
        "#911eb4",
        "#46f0f0",
        "#f032e6",
        "#d2f53c",
        "#fabebe",
        "#008080",
        "#e6beff",
        "#aa6e28",
        "#274c17",
        "#800000",
        "#aaffc3",
        "#808000",
        "#ffd8b1",
        "#000080",
        "#808080",
        "#469638",
        "#609848",
    ];

    return colorArray;
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function drawPieTaxonomy(){
    var ctx = document.getElementById("myChart-viral-taxonomy").getContext('2d');
    $.getJSON( "/getTaxonomyDistribution", function(jsondata){
        if (typeof currentChart !== 'undefined') {
            currentChart.destroy();
        }
        currentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: jsondata["data"],
                    backgroundColor: getColors(jsondata["data"].length),
                }],
                labels: jsondata["labels"],
            },
            options: {
                pieceLabel: {
                    render: 'percentage',
                    fontColor: function (data) {
                        var rgb = hexToRgb(data.dataset.backgroundColor[data.index]);
                        var threshold = 140;
                        var luminance = 0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b;
                        return luminance > threshold ? 'black' : 'white';
                    },
                    precision: 2
                }, legend: {
                    onClick:
                    function(e, legendItem) {
                        var index = legendItem.index;
                        var ci = this.chart;
                        var meta = ci.getDatasetMeta(0);
                        var currentAlreadyHidden = (meta.data[index].hidden==null) ? false : (meta.data[index].hidden);

                        var label = meta.data[index]._model.label;
                        if (currentAlreadyHidden) {
                            // add tag back to graph and table
                            meta.data[index].hidden=false;
                            filteredViralTax = filteredViralTax.filter(x => !x.includes(label))

                        } else {
                            meta.data[index].hidden=true;
                            filteredViralTax.push(`'`+label+`'`);

                        }
                        if (filteredViralTax.length == 7) {
                            document.getElementById("family-chart-header").innerHTML = "Showing Top 5 Families for Realm " + label;
                            realm = label;
                            drawFamilyPieTaxonomy(label);
                            return;
                        } else {
                            if (filteredViralTax.length == 0) {
                                filteredViralTax = ["''"]
                            }
                            buildHtmlTable('#taxTable');
                        }
                        ci.update();
                    }
                }
            }
        });
        $("#table-section").removeClass('hidden');
    });
}

function drawFamilyPieTaxonomy(realm) {
    var ctx = document.getElementById("myChart-viral-taxonomy").getContext('2d');
    $.getJSON( "/getFamilyTaxonomyDistribution/" + realm + "/(" + familyList.join(",") + ")", function(jsondata){
            // add the top 5 families (labels) to familyList first
            for (const fam of jsondata['labels']) {
                familyList.push(`'`+fam+`'`);
            }
            console.log(familyList)
            // destroy current chart and create new chart for families in 'realm'
            currentChart.destroy();
            currentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: jsondata["data"],
                    backgroundColor: getColors(jsondata["data"].length),
                }],
                labels: jsondata["labels"],
            },
            options: {
                pieceLabel: {
                    render: 'percentage',
                    fontColor: function (data) {
                        var rgb = hexToRgb(data.dataset.backgroundColor[data.index]);
                        var threshold = 140;
                        var luminance = 0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b;
                        return luminance > threshold ? 'black' : 'white';
                    },
                    precision: 2
                }, legend: {
                    onClick:
                    function(e, legendItem) {
                        var index = legendItem.index;
                        var ci = this.chart;
                        var meta = ci.getDatasetMeta(0);
                        var currentAlreadyHidden = (meta.data[index].hidden==null) ? false : (meta.data[index].hidden);

                        if (currentAlreadyHidden) {
                            // add tag back to graph and table
                            meta.data[index].hidden=false;
                            var label = meta.data[index]._model.label;
                            filteredViralTax = filteredViralTax.filter(x => !x.includes(label))
                            familyList.push(`'`+label+`'`);
                        } else {
                            meta.data[index].hidden=true;
                            var label = meta.data[index]._model.label;
                            filteredViralTax.push(`'`+label+`'`);
                            familyList = familyList.filter(x => !x.includes(label))
                        }
                        ci.update();
                        if (filteredViralTax.length == 0) {
                            filteredViralTax = ["''"]
                        }
                        buildHtmlTable('#taxTable');
                        console.log(familyList)
                    }
                }
            }
        }); 
        buildHtmlTable('#taxTable');
        createFamilyOptions();
        $("#family-chart").removeClass('hidden');
    });
}

function viralTaxSelectAll() {
    familyList = ["''"];
    currentChart.getDatasetMeta(0).data.forEach(function(ds) {
        ds.hidden = false;
        if (realm != "") {
            familyList.push(`'`+ds._model.label+`'`);
        };
    });
    filteredViralTax = ["''"];
    currentChart.update();
    buildHtmlTable('#taxTable');
}

function viralTaxDeselectAll() {
    filteredViralTax = ["''"];
    currentChart.getDatasetMeta(0).data.forEach(function(ds) {
        ds.hidden = true;
        filteredViralTax.push(`'`+ds._model.label+`'`)
    });
    familyList = ["''"];
    currentChart.update();
    buildHtmlTable('#taxTable');
}

function viralTaxReset() {
    filteredViralTax = ["''"];
    familyList = ["''"];
    realm = "";
    document.getElementById("family-chart-header").innerHTML = "";
    $("#family-chart").addClass('hidden');
    drawPieTaxonomy();
    buildHtmlTable('#taxTable');
}

// Builds the HTML Table out of myList
function buildHtmlTable(selector) {
    query = "/filteredTaxonomyData/(" + filteredViralTax.join(",") + ")"
    if (realm != "") {
        query = query + "/(" + familyList.join(",") + ")"
    }
    $(selector).DataTable( {
        processing: true,
        serverSide: true,
        ajax: query,
        destroy: true,
        columns: [
            { title: "Accession ID"},
            { title: "Scientific Name"},
            { title: "Length" },
            { title: "Organism" },
            { title: "Realm" },
            { title: "Family" }
        ]
    });
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records.
function addAllColumnHeaders(jsondata, selector) {
    var headerTr$ = $('<tr/>');

    var cols = Object.values(jsondata);
    var keys = Object.keys(cols[0]);
    for (var i = 0; i < keys.length; i++) {
        cols.push(keys[i]);
        headerTr$.prepend($('<th/>').html(keys[i]));
    }
    $("#taxTable").append($('<thead/>').append(headerTr$));
}
