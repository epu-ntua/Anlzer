/**
 * Created by DarkA_000 on 3/31/2016.
 */

(function(exports) {

    // Append or remove a loading .gif depending on whether it's present or not
    exports.toggleLoading = function() {
        var $body = $('body'),
            $loading = $body.children('.form-loading');

        if ($loading.length == 0)
            $body.append('<div class="form-loading"></div>');
        else
            $loading.remove()
    };

    // disabled the submit button while the request is processing
    exports.disableSubmit = function(form) {
        var $form = $(form);

        $form
            .find('input, button')
            .filter('[type="submit"]')
            .attr('disabled', 'disabled');

        return $(form)
    };
    

    /* actually submit the form. The only restriction is that the form
    * must have a valid id tag else jQuery won't be able to guarantee
    * that the form gets reproduced with its errors in a correct way
    */
    exports.post = function(form) {

        exports.toggleLoading();
        
        var $form = $(form),
            $submit = $(form).find('[type="submit"]'),
            data =  new FormData(form[0]),
            url =  $form.attr('action'),
            id = $form.attr('id');
        
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            async: true,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data, textStatus, xhr) {
                exports.toggleLoading();

                // If the object has not been created via the previous POST
                if (xhr.status != 204) {
                    $('html')
                        .find('form[id="' + id + '"]')
                        .replaceWith(($(data)
                            .find('form[id="' + id + '"]')));

                    // Calls all the modules that need to be re-initialized
                    moduleManager.call()
                }
                // If the object was successfully posted, check if the object creation has another step to go to
                // by checking whether the submit btn has such attributes
                else {

                    // Reset the inputs of the form since the DOM isn't updated on JS success
                    $form[0].reset();
                    
                }
            },
            error: function (xhr, status, error) {
                console.log('An Error has occured');
                exports.toggleLoading();
            }
        })
    }
})(this.ajaxFormManager = {});
