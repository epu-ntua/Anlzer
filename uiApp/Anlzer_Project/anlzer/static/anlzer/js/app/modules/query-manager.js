/**
 * Created by DarkA_000 on 6/10/2016.
 */

(function(exports) {

    exports.get = function(project_pk, report_pk, filters, endpoint, callback) {

        $.ajax({
            url: '/anlzer/api/projects/' + project_pk + '/reports/' + report_pk + '/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                exports.send(data, endpoint, filters, callback);
            },
            error: function (xhr, status, error) {
                console.log('An Error has occured on the report info request');
            }
         });
    };

    exports.send = function(api_object, endpoint, filters, callback) {

        var localEndpoint = (!endpoint) ? 'basic_stats' : endpoint,
            url = 'http://146.185.171.237:8282/anlzer/api/v1.0/' + localEndpoint + '/',
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
        }
        console.log(query_string)
         $.ajax({
            url: url + query_string,
            type: 'GET',
            dataType: 'json',
            success: function (data, textStatus, xhr) {
                (callback) ? callback(data) : true;
            },
            error: function (xhr, status, error) {
                console.log('An Error has occured on the engine result receival');
            }
         });

        return exports
    };

    exports.call = function() {
        for (var i = 0; i < fns.length; i++) {
            fns[i]();
        }
        return fns;
    }
})(this.queryManager = {});