/**
 * Created by evi on 19/6/2016.
 */


$(document).ready(function() {

    var currentUrl = window.location.href,
        projectPk = parseInt(currentUrl.split('/projects/')[1].split('/')[0]),
        reportPk = parseInt(currentUrl.split('/reports/')[1].split('/')[0]),
        $body = $('body');

    var svg_g;
    var svg_s;

    // useful for pie charts
    function generateChartData(types,selected) {
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

    /* start of: callback functions for engine results */

    function sentiwords(data) {
        var frequency_list = [];
        // add triples of the form {"size": 5,"sentiment":"angry","text": "wicked"} to the array
        $.each(data.sentiments, function (k1, v1) {
            $.each(v1, function (k2, v2) {
                if ((v2.key !== "_url") && (v2.key !== "_username") && (v2.key !== "rt")) {
                    frequency_list.push({"size": v2.doc_count, "sentiment": k1, "text": v2.key});
                }
            })});


        var color = d3.scale.ordinal()
            .domain([0, 1, 2, 3, 4])
            .range(["#ffa500", "#008000", "#5e5e5e", "#a52a2a", "#ff0000"]);
        //"#ff0000", "#a52a2a", "#050505", "#008000", "#ffa500",

        // TODO: this is a function to normalize a bit the size differences...maybe there is a better way
        function assign_font_size(count) {
            var sizes = frequency_list.map(function (a) {
                return a.size;
            });
            var min = Math.min.apply(null, sizes),
                max = Math.max.apply(null, sizes);
            var absmax = 60
            var absmin = 15
            if (max == 1) return min
            var font = Math.log(count) / Math.log(max) * (max - min) + min
            var finalfont = (((font - min) * (absmax - absmin)) / (max - min)) + absmin
            return finalfont
        }

        function assign_col(sentiment) {
            if (sentiment == "excited")
                return 0
            else if (sentiment == "happy")
                return 1
            else if (sentiment == "neutral")
                return 2
            else if (sentiment == "sad")
                return 3
            else return 4
        }

        for (var i = 0; i < frequency_list.length; i++) {
            frequency_list[i].size = assign_font_size(frequency_list[i].size)
        }

        d3.layout.cloud().size([450, 400])
            .words(frequency_list)
            .rotate(0)
            .fontSize(function (d) {
                return d.size;
            })
            .on("end", draw)
            .start();

        function draw(words) {
            svg_s = d3.select("#sentiwordclouddd").append("svg");
            svg_s.attr("width", 500)
                .attr("height", 450)
                .attr("class", "wordcloud")
                .append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(200,220)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function (d) {
                    return d.size + "px";
                })
                .style("fill", function (d, i) {
                    return color(assign_col(d.sentiment))
                })
                .attr("transform", function (d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function (d) {
                    return d.text;
                });
        };

    };

    function update_sentiwords(data) {
        var frequency_list = [];
        // add triples of the form {"size": 5,"sentiment":"angry","text": "wicked"} to the array
        $.each(data.sentiments, function (k1, v1) {
            $.each(v1, function (k2, v2) {
                if ((v2.key !== "_url") && (v2.key !== "_username") && (v2.key !== "rt")) {
                    frequency_list.push({"size": v2.doc_count, "sentiment": k1, "text": v2.key});
                }
            })});


        var color = d3.scale.ordinal()
            .domain([0, 1, 2, 3, 4])
            .range(["#ffa500", "#008000", "#5e5e5e", "#a52a2a", "#ff0000"]);

        // TODO: this is a function to normalize a bit the size differences...maybe there is a better way
        function assign_font_size(count) {
            var sizes = frequency_list.map(function (a) {
                return a.size;
            });
            var min = Math.min.apply(null, sizes),
                max = Math.max.apply(null, sizes);
            var absmax = 60
            var absmin = 15
            if (max == 1) return min
            var font = Math.log(count) / Math.log(max) * (max - min) + min
            var finalfont = (((font - min) * (absmax - absmin)) / (max - min)) + absmin
            return finalfont
        }

        function assign_col(sentiment) {
            if (sentiment == "excited")
                return 0
            else if (sentiment == "happy")
                return 1
            else if (sentiment == "neutral")
                return 2
            else if (sentiment == "sad")
                return 3
            else return 4
        }

        for (var i = 0; i < frequency_list.length; i++) {
            frequency_list[i].size = assign_font_size(frequency_list[i].size)
        }

        d3.layout.cloud().size([450, 400])
            .words(frequency_list)
            .rotate(0)
            .fontSize(function (d) {
                return d.size;
            })
            .on("end", draw)
            .start();

        function draw(words) {
            svg_s.remove();
            svg_s = d3.select("#sentiwordclouddd").append("svg");
            svg_s.attr("width", 500)
                .attr("height", 450)
                .attr("class", "wordcloud")
                .append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(160,220)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function (d) {
                    return d.size + "px";
                })
                .style("fill", function (d, i) {
                    return color(assign_col(d.sentiment))
                })
                .attr("transform", function (d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function (d) {
                    return d.text;
                });
        };

    };

    function pspairssentiprocess(data) {
        var dataProvider = [];
        $.each(data.services, function (k1, v1) {
            var title_second = v1.key;
            $.each(v1.products.buckets, function (k2, v2) {
                var array_object = {};
                var title_first = v2.key;
                array_object["P-S"] = title_first+"-"+title_second;
                $.each(v2.sentiment.buckets, function (k3, v3) {
                    array_object[v3.key] = v3.doc_count;
                });
                dataProvider.push(array_object);
            });
            var padding = 5 - dataProvider.length;
            for (var i=0; i<padding; i++){
                dataProvider.push(
                    {
                        "P-S": "",
                        "angry": 0,
                        "sad": 0,
                        "neutral": 0,
                        "happy": 0,
                        "excited": 0
                    }
                )
            }

        });

        AmCharts.makeChart("chartstackdiv", {
            "rotate":true,
            "type": "serial",
            "theme": "light",
            "legend": {
                "horizontalGap": 10,
                "maxColumns": 1,
                "position": "right",
                "useGraphSettings": true,
                "markerSize": 10
            },
            "dataProvider": dataProvider,
            "valueAxes": [{
                "stackType": "regular",
                "axisAlpha": 0.3,
                "gridAlpha": 0
            }],
            "graphs": [{
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "angry",
                "type": "column",
                "color": "#000000",
                "valueField": "angry"
            }, {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "sad",
                "type": "column",
                "color": "#000000",
                "valueField": "sad"
            }, {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "neutral",
                "type": "column",
                "color": "#000000",
                "valueField": "neutral"
            }, {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "happy",
                "type": "column",
                "color": "#000000",
                "valueField": "happy"
            }, {
                "balloonText": "<b>[[title]]</b><br><span style='font-size:14px'>[[category]]: <b>[[value]]</b></span>",
                "fillAlphas": 0.8,
                "labelText": "[[value]]",
                "lineAlpha": 0.3,
                "title": "excited",
                "type": "column",
                "color": "#000000",
                "valueField": "excited"
            }],
            "categoryField": "P-S",
            "categoryAxis": {
                "gridPosition": "start",
                "axisAlpha": 0,
                "gridAlpha": 0,
                "position": "left"
            },
            "export": {
                "enabled": true
            }

        });

    };

    function process_productsser_data(data) {
        var selected;
        var products = [];
        var total_prod_count = 0;
        var subs = {};

        $.each(data.products, function (k1, v1) {
            total_prod_count += v1.doc_count;
        });

        $.each(data.products, function (k1, v1) {
            products.push({"type":v1.key,"percent":(100*v1.doc_count/total_prod_count).toFixed(0)});
        });

        $.each(data.products, function (k1, v1) {
            var words = [];
            var remaining = v1.doc_count;
            $.each(v1.services.buckets, function (k2, v2) {
                remaining -= v2.doc_count
                words.push({"type":v2.key,"percent":(100*v2.doc_count/total_prod_count).toFixed(0)});
            });
            words.push({"type":"no service","percent":(100*remaining/total_prod_count).toFixed(0)});
            subs[v1.key] = words;
        });

        for (var i=0;i<products.length;i++){
            products[i].subs = subs[products[i].type];
        }

        AmCharts.makeChart("chartdiv2", {
            "autoMargins": false,
            "type": "pie",
            "dataProvider": generateChartData(products,selected),
            "labelText": "[[title]]: [[value]]",
            "balloonText": "[[title]]: [[value]]",
            "titleField": "type",
            "valueField": "percent",
            "outlineColor": "#d3d3d3",
            "color": "#0d0d0d",
            "baseColor": "#5500FF",
            "labelTickColor": "#0d0d0d",
            "labelsEnabled": true,
            "radius": "20%",
            "outlineAlpha": 0.8,
            "outlineThickness": 2,
            "colorField": "color",
            "pulledField": "pulled",
            "titles": [{
                "text": "PRODUCTS \n(click on pie to see related services)"
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
                    chart.dataProvider = generateChartData(products,selected);
                    chart.validateData();
                }
            }]
        });

    };

    function process_servicespro_data(data) {
        var selected;
        var services = [];
        var total_serv_count = 0;
        var subs = {};

        $.each(data.services, function (k1, v1) {
            total_serv_count += v1.doc_count;
        });

        $.each(data.services, function (k1, v1) {
            services.push({"type":v1.key,"percent":(100*v1.doc_count/total_serv_count).toFixed(0)});
        });

        $.each(data.services, function (k1, v1) {
            var words = [];
            var remaining = v1.doc_count;
            $.each(v1.products.buckets, function (k2, v2) {
                remaining -= v2.doc_count
                words.push({"type":v2.key,"percent":(100*v2.doc_count/total_serv_count).toFixed(0)});
            });
            words.push({"type":"no product","percent":(100*remaining/total_serv_count).toFixed(0)});
            subs[v1.key] = words;
        });

        for (var i=0;i<services.length;i++){
            services[i].subs = subs[services[i].type];
        }

        AmCharts.makeChart("chartdiv", {
            "autoMargins": false,
            "type": "pie",
            "dataProvider": generateChartData(services,selected),
            "labelText": "[[title]]: [[value]]",
            "balloonText": "[[title]]: [[value]]",
            "titleField": "type",
            "valueField": "percent",
            "outlineColor": "#d3d3d3",
            "color": "#0d0d0d",
            "baseColor": "#FF004A",
            "labelTickColor": "#0d0d0d",
            "labelsEnabled": true,
            "radius": "20%",
            "outlineAlpha": 0.8,
            "outlineThickness": 2,
            "colorField": "color",
            "pulledField": "pulled",
            "titles": [{
                "text": "SERVICES \n(click on pie to see related products)"
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
                    chart.dataProvider = generateChartData(services,selected);
                    chart.validateData();
                }
            }]
        });

    };

    function process_timeline_data(data) {

        dataProvider = []

        $.each(data.results.daily_results.buckets, function (k1, v1) {
            dataProvider.push({"date":v1.key_as_string,"value":v1.doc_count});
        });

        var chart = AmCharts.makeChart("charttimelinediv", {
            "type": "serial",
            "theme": "light-emo",
            "marginRight": 40,
            "marginLeft": 40,
            "autoMarginOffset": 20,
            "mouseWheelZoomEnabled":true,
            "dataDateFormat": "YYYY-MM-DD",
            "legend": {
                "useGraphSettings": true
            },
            "valueAxes": [{
                "id": "v1",
                "axisAlpha": 0,
                "position": "left",
                "ignoreAxisWidth":true
            }],
            "balloon": {
                "borderThickness": 1,
                "shadowAlpha": 0
            },
            "graphs": [{
                "id": "g1",
                "balloon":{
                    "drop":true,
                    "adjustBorderColor":false,
                    "color":"#ffffff"
                },
                "bullet": "round",
                "bulletBorderAlpha": 1,
                "bulletColor": "#FFFFFF",
                "bulletSize": 5,
                "hideBulletsCount": 50,
                "lineThickness": 2,
                "title": "all",
                "useLineColorForBulletBorder": true,
                "valueField": "value",
                "balloonText": "<span style='font-size:18px;'>[[value]]</span>"
            }],
            "chartScrollbar": {
                "graph": "g1",
                "oppositeAxis":false,
                "offset":30,
                "scrollbarHeight": 80,
                "backgroundAlpha": 0,
                "selectedBackgroundAlpha": 0.1,
                "selectedBackgroundColor": "#888888",
                "graphFillAlpha": 0,
                "graphLineAlpha": 0.5,
                "selectedGraphFillAlpha": 0,
                "selectedGraphLineAlpha": 1,
                "autoGridCount":true,
                "color":"#AAAAAA"
            },
            "chartCursor": {
                "pan": true,
                "valueLineEnabled": true,
                "valueLineBalloonEnabled": true,
                "cursorAlpha":1,
                "cursorColor":"#258cbb",
                "limitToGraph":"g1",
                "valueLineAlpha":0.2,
                "valueZoomable":true
            },
            "valueScrollbar":{
                "oppositeAxis":false,
                "offset":50,
                "scrollbarHeight":10
            },
            "categoryField": "date",
            "categoryAxis": {
                "parseDates": true,
                "dashLength": 1,
                "minorGridEnabled": true
            },
            "export": {
                "enabled": true
            },
            "dataProvider": dataProvider
        });

        chart.addListener("rendered", zoomChart);

        zoomChart();

        function zoomChart() {
            chart.zoomToIndexes(chart.dataProvider.length - 40, chart.dataProvider.length - 1);
        }


    };

    function nouncloud(data) {
        var frequency_list = [];

        $.each(data.nouns, function (k1, v1) {
            if ((v1.key !== "_url") && (v1.key !== "_username") && (v1.key !== "rt")){
                frequency_list.push({"size": v1.doc_count,"text": v1.key});
            }

        });

        var color = d3.scale.linear()
            .domain([0,1,2,3,10,100,1000,10000,100000,4000000])
            .range(["#ccbadc","#bba3d0","#aa8cc5","#9975b9","#885ead","#7647a2","#663096","#551a8b"]);

        // TODO: this is a function to normalize a bit the size differences...maybe there is a better way
        function assign_font_size(count){
            var sizes = frequency_list.map(function(a) {return a.size;});
            var min = Math.min.apply(null, sizes),
                max = Math.max.apply(null, sizes);
            var absmax = 45
            var absmin = 15
            if (max==1) return min
            var font = Math.log(count) / Math.log(max) * (max - min) + min
            var finalfont = (((font - min) * (absmax - absmin)) / (max - min)) + absmin
            return finalfont
        }

        for (var i = 0; i < frequency_list.length; i++) {
            frequency_list[i].size = assign_font_size(frequency_list[i].size)
        }

        d3.layout.cloud().size([950, 450])
            .words(frequency_list)
            .rotate(0)
            .fontSize(function(d) { return d.size; })
            .on("end", draw)
            .start();

        function draw(words) {
            svg_g = d3.select("#nounwordcloud").append("svg");
            svg_g.attr("width", 1000)
                .attr("height", 500)
                .attr("class", "wordcloud")
                .append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(420,260)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.size + "px"; })
                .style("fill", function(d, i) {  return color(i)  })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.text; });
        }
    };

    function update_nouncloud(data) {
        var frequency_list = [];

        $.each(data.nouns, function (k1, v1) {
            if ((v1.key !== "_url") && (v1.key !== "_username") && (v1.key !== "rt")){
                frequency_list.push({"size": v1.doc_count,"text": v1.key});
            }

        });

        var color = d3.scale.linear()
            .domain([0,1,2,3,4,5,6,10,15,20,30,40])
            .range(["#ffa500","#ffae19","#ffb732","#ffc04c","#ffc966","#ffd27f","#ffdb99","#ffe4b2"]);

        // TODO: this is a function to normalize a bit the size differences...maybe there is a better way
        function assign_font_size(count){
            var sizes = frequency_list.map(function(a) {return a.size;});
            var min = Math.min.apply(null, sizes),
                max = Math.max.apply(null, sizes);
            var absmax = 45
            var absmin = 15
            if (max==1) return min
            var font = Math.log(count) / Math.log(max) * (max - min) + min
            var finalfont = (((font - min) * (absmax - absmin)) / (max - min)) + absmin
            return finalfont
        }

        for (var i = 0; i < frequency_list.length; i++) {
            frequency_list[i].size = assign_font_size(frequency_list[i].size)
        }

        d3.layout.cloud().size([950, 450])
            .words(frequency_list)
            .rotate(0)
            .fontSize(function(d) { return d.size; })
            .on("end", draw)
            .start();

        function draw(words) {
            svg_g.remove();
            svg_g = d3.select("#nounwordcloud").append("svg");
            svg_g.attr("width", 1000)
                .attr("height", 500)
                .attr("class", "wordcloud")
                .append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(420,260)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.size + "px"; })
                .style("fill", function(d, i) {  return color(i)  })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.text; });
        }
    };

    function evalOverviewFilters() {
        var langList = $('input.icheck[name="language-filter"]').map(function() {
            return ($(this).is(':checked')) ? $(this).val() : null;
        }).get().join();

        var infMode = $('input.switchbox[name="influencer-mode"]').is(':checked')

        return {
            'influencer_mode': infMode,
            'language': langList
        }
    };

    // evaluates the filters inside the overview page and returns them in a nice JS Object
    function createAllCharts(projectId , reportId, filters) {
        queryManager.get(projectId, reportId, filters, 'sentiwords', sentiwords);
        queryManager.get(projectId, reportId, filters, 'productsser', process_productsser_data);
        queryManager.get(projectId, reportId, filters, 'servicespro', process_servicespro_data);
        queryManager.get(projectId, reportId, filters, 'nouns', nouncloud);
        queryManager.get(projectId, reportId, filters, 'pspairsenti', pspairssentiprocess);
        queryManager.get(projectId, reportId, filters, 'daily_histogram', process_timeline_data);
        sf.get(projectId, reportId, filters, sf.dothework);
    }

    function updateAllCharts(projectId , reportId, filters) {
        queryManager.get(projectId, reportId, filters, 'sentiwords', update_sentiwords);
        queryManager.get(projectId, reportId, filters, 'productsser', process_productsser_data);
        queryManager.get(projectId, reportId, filters, 'servicespro', process_servicespro_data);
        queryManager.get(projectId, reportId, filters, 'nouns', update_nouncloud);
        queryManager.get(projectId, reportId, filters, 'pspairsenti', pspairssentiprocess);
        queryManager.get(projectId, reportId, filters, 'daily_histogram', process_timeline_data);
        sf.get(projectId, reportId, filters, sf.dothework);
    }

    // initial call
    createAllCharts(projectPk, reportPk, {});

    // update the overview each time the influencer mode is toggled
    $body.on('ifToggled', '.icheck', function() {
        updateAllCharts(projectPk, reportPk, evalOverviewFilters());
    });

    // update the overview each time a language is added or removed
    $body.on('switchChange.bootstrapSwitch', '.switchbox', function() {
        updateAllCharts(projectPk, reportPk, evalOverviewFilters());
    });


    /* end of: callback functions for engine results */

});