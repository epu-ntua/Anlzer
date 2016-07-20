/**
 * Created by evi on 19/6/2016.
 */

(function myse(sf) {
    var url_start = 'http://146.185.171.237:8282/anlzer/api/v1.0/';
    var total = 0;
    var query_string = "";
    var counts = {
        "angry": 0,
        "sad": 0,
        "neutral": 0,
        "happy": 0,
        "excited": 0
    };

//initialization with emotion values and corrresponding colours
//this array is required by the pie chart
    var sentiments = [
        {
            type: "excited",
            color: "#ffa500"
        },
        {
            type: "happy",
            color: "#008000"
        }, {
            type: "neutral",
            color: "#5e5e5e"
        },
        {
            type: "sad",
            color: "#a52a2a"
        },
        {
            type: "angry",
            color: "#ff0000"
        }
    ];

//get total number of docs for each sentiment and add percentages to "sentiments" array used by chart
    function processgeneral(data) {
        $.each(data.sentiments, function (k1, v1) {
            counts[k1] = v1;
            total += v1;
        });
        //TODO think of weird percentage combos and check how chart is affected
        for (var i = 0; i < sentiments.length; i++) {
            sentiments[i].percent = (100 * counts[sentiments[i].type] / total).toFixed(0);
        }
        getspecifics();

    }

    function getgeneralstats(){
        //return
        $.ajax({
        url: url_start + 'sentiments/' + query_string,
        dataType: 'json',
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Error getting response from server. Text status: " + textStatus + ". Error thrown: " + errorThrown);
        },
        success: processgeneral
    });};

    function getspecifics() {
        $.ajax({
            url: url_start + 'sentiwords/' + query_string,
            dataType: 'json',
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error getting response from server. Text status: " + textStatus + ". Error thrown: " + errorThrown);
            },
            success: function (data) {
                var chart;
                var legend;
                var selected;
                var subs = {};

                //TODO correct the round errors in percentages
                $.each(data.sentiments, function (k1, v1) {
                    var words = [];
                    var remaining = counts[k1];
                    $.each(v1, function (k2, v2) {
                        remaining -= v2.doc_count
                        words.push({"type": v2.key, "percent": (100 * v2.doc_count / total).toFixed(0)});
                    });
                    //correct the percentages by adding a "other" option to the pie, for the reamining docs
                    words.push({"type": "other", "percent": (100 * remaining / total).toFixed(0)});
                    subs[k1] = words;
                });

                for (var i = 0; i < sentiments.length; i++) {
                    sentiments[i].subs = subs[sentiments[i].type];
                }

                function generateChartData(types) {
                    var chartData = [];
                    for (var i = 0; i < types.length; i++) {
                        if (i == selected) {
                            for (var x = 0; x < types[i].subs.length; x++) {
                                chartData.push({
                                    type: types[i].subs[x].type,
                                    percent: types[i].subs[x].percent,
                                    color: types[i].color,
                                    pulled: true
                                });
                            }
                        } else {
                            chartData.push({
                                type: types[i].type,
                                percent: types[i].percent,
                                color: types[i].color,
                                id: i
                            });
                        }
                    }
                    return chartData;
                }


                AmCharts.makeChart("sentichartdiv", {
                    "autoMargins": false,
                    "type": "pie",
                    "dataProvider": generateChartData(sentiments),
                    "labelText": "[[title]]: [[value]]",
                    "balloonText": "[[title]]: [[value]]",
                    "titleField": "type",
                    "valueField": "percent",
                    "outlineColor": "#d3d3d3",
                    "color": "#0d0d0d",
                    //"baseColor":"#ff9e01",
                    "labelTickColor": "#0d0d0d",
                    "labelsEnabled": true,
                    //"radius":"25%",
                    "outlineAlpha": 0.8,
                    "outlineThickness": 2,
                    "colorField": "color",
                    "pulledField": "pulled",
                    "titles": [{
                        "text": "Sentiments \n(Click on pie to see top related terms)"
                    }],
                    "listeners": [{
                        "event": "clickSlice",
                        "method": function (event) {
                            var chart = event.chart;
                            if (event.dataItem.dataContext.id != undefined) {
                                selected = event.dataItem.dataContext.id;
                            } else {
                                selected = undefined;
                            }
                            chart.dataProvider = generateChartData(sentiments);
                            chart.validateData();
                        }
                    }]
                });

            }
        });
    };

    sf.dothework = function(){
        getgeneralstats();
    };

    sf.get = function(project_pk, report_pk, filters,callback){
        $.ajax({
            url: '/anlzer/api/projects/' + project_pk + '/reports/' + report_pk + '/',
            type: 'GET',
            dataType: 'json',
            success: function (api_object) {
                query_string = '?';
                query_string += ('pk' in api_object) ? 'pid=' + api_object['pk'] : '';
                query_string += ('start_date' in api_object) ? '&start=' + api_object['start_date'] : '';
                query_string += ('end_date' in api_object) ? '&end=' + api_object['end_date'] : '';
                query_string += ('hashtags' in api_object) ? '&hashtags="' + api_object['hashtags'] + '"' : '""';
                query_string += ('pages' in api_object) ? '&pages="' + api_object['pages'] + '"' : '""';
                query_string += ('providers' in api_object) ? '&sources="' + api_object['providers'] + '"' : '""';

                if (filters) {
                    query_string += ('influencer_mode' in filters) ? '&infmode=' + filters['influencer_mode'].toString() : '';
                    query_string += ('language' in filters) ? '&language="' + filters['language']  + '"' : '';
                };
                callback();

            },
            error: function (xhr, status, error) {
                console.log('An Error has occured on the report info request');
            }
        });

    }
}(this.sf = {}));

//    example of array to be created for the chart...
//var sentiments_model = [
//                {
//                    type: "excited",
//                    percent: 15,
//                    color: "#ffff00",
//                    subs: [{
//                        type: "beautiful",
//                        percent: 10
//                    }, {
//                        type: "love",
//                        percent: 5
//                    }]
//                },
//                {
//                    type: "happy",
//                    percent: 50,
//                    color: "#00b200",
//                    subs: [{
//                        type: "comfortable",
//                        percent: 8
//                    }, {
//                        type: "fabulous",
//                        percent: 35
//                    }, {
//                        type: "colour",
//                        percent: 7
//                    }]
//                }, {
//                    type: "neutral",
//                    percent: 5,
//                    color: "#d3d3d3",
//                    subs: [{
//                        type: "interiordesign",
//                        percent: 5
//                    }]
//
//                },
//                {
//                    type: "sad",
//                    percent: 9,
//                    color: "#b20000",
//                    subs: [{
//                        type: "counterintuitive",
//                        percent: 9
//                    }]
//
//                },
//                {
//                    type: "angry",
//                    percent: 21,
//                    color: "#ff0000",
//                    subs: [{
//                        type: "open",
//                        percent: 15
//                    },
//                        {
//                            type: "simple",
//                            percent: 6
//                        }]
//
//                }
//            ];