/**
 * Created by DarkA_000 on 4/8/2016.
 */

/*
 =======================================
 Handlers for content related to Reports
 =======================================

 1. Handler for the live switch (On/Off)
 2. Handler that managers the population of the sources through the project sources during report creation
 3. Handler for Daterangepicker appearance
 4. Handler for the popover in a report details, for correcting the sentiment

 */


$(window).on('load', function() {
    var $body = $('body'),
        $reportForm = $('form.report-creation-form, form.report-update-form'), // only 1 of these will ever be chosen
        $liveSwitchbox = $reportForm.find('.live-report-switchbox'),
        $fixedRangeInput = $reportForm.find('p.fixed-range'),
        $liveRangeInput = $reportForm.find('p.live-range'),
        $liveHelpText = $reportForm.find('.help-text.live-text'),
        $sourceOptions = $reportForm.find('.source-option');

    /* Toggle live or fixed date range depending on the status of the "Live" switchbox */
    $liveSwitchbox.on('switchChange.bootstrapSwitch', function() {
        if ($liveSwitchbox.is(':checked'))
            $fixedRangeInput.fadeOut('fast', function () {
                $liveRangeInput.fadeIn('fast');
                $liveHelpText.slideDown('fast')

            });
        else
            $liveRangeInput.fadeOut('fast', function () {
                $fixedRangeInput.fadeIn('fast');
                $liveHelpText.slideUp('fast')
            })
    });

    /* Handler for the source options on Report Creation */
    $sourceOptions.on('click', function() {
        var $this = $(this),
            id = $this.prop('id');

        // remove the active class from the previous option
        $sourceOptions.not(this).removeClass('active');

        // If it was active from before, do nothing
        if ($this.hasClass('active'))
            return;
        else
            $this.addClass('active');
        
        // If we chose the "Use Project Sources" option, we make the inputs dissapear,
        // request from the server the sources of the project and finally fill the inputs and selects with
        // these options
        if ((id == "use-project-sources") || (id == 'modify-project-sources')) {

            // hide the inputs if the option was "user-project-sources"
            (id == "use-project-sources") ? $body.find('.fields-container.step2-fields').fadeOut('slow') : true;
            
            // request the data of the Project and append them in the input
            $.ajax({
                type: 'GET',
                url: '/anlzer/api/projects/' + $reportForm.data('project') + '/sources/',
                async: true,
                contentType: 'json',
                success: function (data, textStatus, xhr) {
                    var $pages = $('input[id*="pages"].anlzer-tokenfield'),
                        $hashtags = $('input[id*="hashtags"].anlzer-tokenfield'),
                        $provider = $('select[id*="provider"]'),
                        projectProvider = data['provider'];

                    // Replicate the pages & the hashtags
                    $pages.tokenfield('setTokens', data['pages']);
                    $hashtags.tokenfield('setTokens', data['hashtags']);

                    // Replicate the selected providers
                    $.each(projectProvider, function(i, provider) {
                        $provider.find('option[value=' + provider + ']').attr('selected', true);
                    });

                    // convert the <select> to a <ul>
                    $provider.selectToUl();
                }
            });
            
            // Show the inputs (if they were hidden before) when the option is "modify-project-sources"
            (id == "modify-project-sources") ? $body.find('.fields-container.step2-fields').fadeIn('slow') : true;
        }
        // Only 1 option left, which is to define custom sources
        else {
            $body
                .find('.fields-container.step2-fields')
                .find('input[id*="pages"].anlzer-tokenfield, input[id*="hashtags"].anlzer-tokenfield, select[id*="provider"]')
                .each(function(i, el) {
                    // try to reset tokenfield
                    if ($(el).is('input'))
                        $(el).tokenfield('setTokens', []);
                    // if its a select element remove everything already selected
                    else
                        $(el).find('option').attr('selected', false);
                });
            
            $('.select-to-ul').selectToUl();
            
            // make the fields appear again
            $body.find('.fields-container.step2-fields').fadeIn('slow')
        }
        
    });

    /* handler for the daterangepicker. It makes sure that the date range is parsed
    *  and the start and end date are assigned to the input fields accordingly
    */
    $('.anlzer-daterangepicker').on('apply.daterangepicker', function(ev, picker) {
          var $startDate = $('#id_start_date'),
              $endDate = $('#id_end_date');

        $startDate.attr('value', picker.startDate.format('MM/DD/YYYY'));
        $endDate.attr('value', picker.endDate.format('MM/DD/YYYY'));
    });


    /*
    *  Handler for the popover that corrects sentiments on the report's detail page
     */
    $body.on('click', '.popover-content .report-icon.correct-sentiment', function(e) {
        var $this = $(this),
            $invoker = $(e.target),
            sentimentClass;
        
    
        console.log($invoker);

        if ($this.hasClass('fa-smile-o'))
            sentimentClass = 'fa-smile-o';
        else if ($this.hasClass('fa-frown-o'))
            sentimentClass = 'fa-frown-o';
        else
            sentimentClass = 'fa-meh-o';

        $this.popover('hide');
        $invoker.removeClass('fa-smile-o fa-frown-o fa-meh-o').addClass(sentimentClass)
    });

    // The init option is use projects sources. On load simulate a click on it
    // but only if we are on the create page
    $('#use-project-sources').trigger('click')
});