/**
 * Created by DarkA_000 on 6/10/2016.
 */


$(document).ready(function() {

    var currentUrl = window.location.href,
        projectPk = parseInt(currentUrl.split('/projects/')[1].split('/')[0]),
        reportPk = parseInt(currentUrl.split('/reports/')[1].split('/')[0]),
        $body = $('body');

    /* start of: callback functions for engine results */

    function truncateBigInteger(number) {
        if (number < 1000)
            return (number).toString();
        else if (number < 10000)
            return (number/1000).toFixed(1) + 'K';
        else if (number < 1000000)
            return (number/1000).toFixed(0) + 'K';
        else if (number < 10000000)
            return (number/1000000).toFixed(1) + 'M';
        else
            return (number/1000000).toFixed(0) + 'M';
    }
    
    function basic_stats(engineResponseObject) {

        var totalDocs = engineResponseObject['total_docs'],
            facebookDocsPcg = parseInt(parseFloat(engineResponseObject['sources']['facebook'])/parseFloat(totalDocs || 1)*100),
            instagramDocsPcg = parseInt(parseFloat(engineResponseObject['sources']['instagram'])/parseFloat(totalDocs || 1)*100),
            twitterDocsPcg = parseInt(parseFloat(engineResponseObject['sources']['twitter'])/parseFloat(totalDocs || 1)*100),
            docsWithKeywordsPcg = parseInt(parseFloat(engineResponseObject['docs_with_all_keywords'])/parseFloat(totalDocs || 1)*100);

    
        $('.total-docs').text(truncateBigInteger(totalDocs));
        $('.keyworded-docs').text(docsWithKeywordsPcg.toString() + '%');
        $('.facebook-docs').text(facebookDocsPcg.toString() + ' %');
        $('.instagram-docs').text(instagramDocsPcg.toString() + ' %');
        $('.twitter-docs').text(twitterDocsPcg.toString() + ' %');
    }

    function top_hashtags(engineResponseObject) {
        
        var $hashtagContainer = $('.term-container');
        if (!engineResponseObject)
            return;
        else
            $hashtagContainer.empty();

        $.each(engineResponseObject['hashtags'], function(i, hashtag) {
            $hashtagContainer.append('<div class="term anlzer-yellow">' + hashtag['name'] + '</div>')
        });
    }

    function sentiments(engineResponseObject) {

        var $donutCirclesContent = $('.donut'),
            sentimentList = engineResponseObject['sentiments'],
            totalDocs = engineResponseObject['total_docs'],
            sentimentPcg,
            sentimentName;

        for (var i=0; i<5; i++) {
            sentimentPcg = parseInt(parseFloat(sentimentList[Object.keys(sentimentList)[i]])/parseFloat(totalDocs || 1)*100),
            sentimentName = Object.keys(sentimentList)[i].toLowerCase();

            $donutCirclesContent
                .filter('.sentiment-' + sentimentName)
                .attr('value', sentimentPcg)
                .knob({
                    'height': 150,
                    'width': 150,
                    'fontWeight': 400,
                    'readOnly': true,
                    'inputColor': '#0aaa76 ',
                    'bgColor': '#f7f7f7',
                    'draw' : function () { $(this.i).val(this.cv + '%'); }
                });
        }
    }

    function evalOverviewFilters() {
        var langList = $('input.icheck[name="language-filter"]').map(function() {
                            return ($(this).is(':checked')) ? $(this).val() : null;
                          }).get().join();

        var infMode = $('input.switchbox[name="influencer-mode"]').is(':checked')

        return {
            'influencer_mode': infMode,
            'language': langList
        }
    }
    
    function updateResults(resultArray) {

        var $container = $('#results'),
            data = resultArray['results']['hits'],
            sentimentDict = {
                'happy': "smile-o green",
                'sad': "frown-o brown",
                'neutral': "meh-o grey",
                'angry': "meh-o red",
                'excited': "smile-o orange"
            };

        $container.empty();
        $.each(data, function(i, dataLine) {
            var line = dataLine['fields'];
            var $htmlObject = '<div class="col-md-12 report-item">' +
                '<div class="col-md-2">' +
                    '<i class="fa fa-' + sentimentDict[line['doc.senti_tag']] + ' report-icon"></i>' +
                '</div>' +
                '<div class=col-md-8>' +
                    '<h3 title="' + line['doc.text'] + '">' + line['doc.text'] + '</h3>' +
                    '<h6>Posted:' + line['doc.created_at'] +  '&nbsp;&#8226;&nbsp; ' +
                        '<i class="fa fa-' + line['doc.source'] + '"></i>' +
                        '&nbsp;&#8226;&nbsp;' + line['doc.user_screen_name'] + '</h6>' +
                '</div>' +
            '</div>';

            $container.append($htmlObject)
        })
    }

    // evaluates the filters inside the overview page and returns them in a nice JS Object
    function updateOverallOverview(projectId , reportId, filters) {
        queryManager.get(projectId, reportId, filters, 'basic_stats', basic_stats);
        queryManager.get(projectId, reportId, filters, 'top_hashtags', top_hashtags);
        queryManager.get(projectId, reportId, filters, 'sentiments', sentiments);
        queryManager.get(projectId, reportId, filters, 'textresults', updateResults);
    }

    // initial call
    updateOverallOverview(projectPk, reportPk, {});

    // update the overview each time the influencer mode is toggled
    $body.on('ifToggled', '.icheck', function() {
        updateOverallOverview(projectPk, reportPk, evalOverviewFilters());
    });

    // update the overview each time a language is added or removed
    $body.on('switchChange.bootstrapSwitch', '.switchbox', function() {
        updateOverallOverview(projectPk, reportPk, evalOverviewFilters());
    });


    /* end of: callback functions for engine results */

});