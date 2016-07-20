/**
 * Created by DarkA_000 on 3/29/2016.
 */


/*
* ========================= Contents ==============================
*
* 1. Handler of the reposition of the hover when the input's position has changed (i.e. tokens added etc)
* 2. Snippet for changing the input to border to red if an error exists in the form
* 3. Handler for Deleting an entry in the database. It submits a form but we want it through a modal
* 
* ====================== End of Contents ==========================
*/


$(document).ready(function() {
    var $body = $('body');

    /*
    * This handler takes care of any form that needs to be send with an
    * asynchronous request to the serve
     */
    // $body.on('submit', 'form.async-form', function(e) {
    //     // Do not send as synchronous
    //     e.preventDefault();
    //     ajaxFormManager.post($(this));
    // });
    /*
    *  End of handler for async form submit
    */

    /*
    * This handlers makes sure the focus repositions (as a yellow line) when new tokens are added in an input field
     */
    $body.on('tokenfield:createdtoken tokenfield:editedtoken tokenfield:removedtoken', '.anlzer-tokenfield', function (e) {
        // The input where tokens are. This is the one that repositioned its height due to token
        // insertion or removal
        var $tokenInput = $(this)
            .closest('.tokenfield')
            .find('.token-input');
        inputFocusManager.reposition($tokenInput)
    });
    /* end of: handler for input focus border reposition */


    /*
    * This handler takes care of any form that needs to be send with an
    * asynchronous request to the serve
     */
    $body.on('click', '.delete-request', function(e) {
        // Do not send as synchronous
        var $this = $(this);

        e.preventDefault();
        $.ajax({
            url: $this.attr('href'),
            type: 'GET',
            async: true,
            cache: false,
            success: function (data, textStatus, xhr) {
                $body.children('.delete-modal').remove();
                $body.append($(data));
                $body.children('.delete-modal').modal('show');
            },
            error: function(xhr) {
                window.location.href= $this.attr('href')
            }
        })
    });
    /*
    *  End of handler for async form submit
    */
});

$(window).load(function() {
    
    /* snippet for changing the input to border to red if an error exists in the form */
    (function() {
        var $errors = $('.errorlist'),
            $djangoFormErrors = $('.django-form-error'),
            errorCSS = {
                'border': ' 1px solid #D90000',
                'background': 'rgba(255, 0, 0, 0.1)'
            };

        $errors.each(function(i, error) {
            $(error)
                .prev()
                .find('label')
                .each(function(i, input) {
                    $(input).css(errorCSS)
                })
        });

        if ($djangoFormErrors.length > 0) {
            $djangoFormErrors
                .closest('form')
                .find('label')
                .each(function(i, input) {
                    $(input).css(errorCSS)
                })
        }
    })();
    /* end of: snipet for errors*/
    
});