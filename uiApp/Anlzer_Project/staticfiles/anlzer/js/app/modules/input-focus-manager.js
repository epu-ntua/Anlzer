/**
 * Created by DarkA_000 on 3/31/2016.
 */


/*
* This handler is responsible for creating the yellow underline that
* appears when you focus on any input inside the Anlzer application
*/
(function(exports) {

    exports.initialize = function () {
        var $body = $('body');

        $body.on('focus.inputFocus', 'input:not(:checkbox), textarea', function () {
            var $this = $(this);

            // If it doesnt belong in an anlzer form do nothing
            if ($this.closest('.anlzer-form').length == 0)
                return;

            // get the width of input and create a dummy element
            var width = $this.innerWidth(),
                height = $this.innerHeight(),
                left = $this.offset().left,
                top = $this.offset().top,
                $after = $('<span class="input-focus"></span>');

            // append it after the current input
            $body.append($after);

            // update the label as focused
            $this.siblings('label').addClass('focus');

            $after
                // assign it some css classes
                .css({
                    display: 'block',
                    margin: 'auto',
                    height: '3px',
                    width: 0,
                    background: '#FFBF02',
                    position: 'absolute',
                    left: left + width / 2,
                    top: top + height
                })
                // animate its width to the width of the input
                .animate(
                    {
                        width: width,
                        left: left
                    },
                    300,
                    'linear'
                );

            // when we change the focus, animate the dummy element back to 0, remove it & close the handler
            $this.on('focusout.inputFocus', function () {

                $after.animate(
                    {
                        width: 0,
                        left: left + width / 2
                    },
                    300,
                    'linear',
                    function () {
                        $after.remove()
                    }
                );

                $this.siblings('label').removeClass('focus');
                $this.off('focusout');
            })
        });

        return exports
    };

    exports.reposition = function (input) {
        var $this = $(input),
            $active = $('.input-focus'),
            height = $this.innerHeight(),
            left = $this.offset().left,
            top = $this.offset().top;

        $active.css({
            left: left,
            top: top + height
        });

        return exports;
    };

    exports.destroy = function() {
        var $active = $('.input-focus'),
            $elems = $('input, textarea, select');

        $active.remove();
        $elems.off('.inputFocus');
        return exports
    };

    exports.reset = function() {
        exports.destroy().initialize();
        return exports
    }
    
})(this.inputFocusManager = {});
/*
* End of handler for inputs inside the Anlzer app
*/