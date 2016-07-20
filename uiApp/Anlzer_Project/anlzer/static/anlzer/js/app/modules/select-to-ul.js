/**
 * Created by DarkA_000 on 4/11/2016.
 */

/*
The purpose of this script is to transform select-type inputs in to <ul> in order to be CSS stylable.
It creates a ul from each select it finds and makes sure they are synced with each other
 */


(function ( $ ) {

    $.fn.selectToUl = function(option) {

        // checks if the select has a corresponding UL
        function UlExists(select) {
            var $select = $(select),
                $ul = $('ul').filter(function() {
                    return ($(this).data('bind') == $select.prop('id'))
                });

            return ($ul.length > 0) ? true : false
        }

        // creates a new UL from a Select-type input
        function createUlFromSelect(select) {

            // We destroy the previous ul and re-build it
            if (UlExists(select))
                    destroy(select);

            var $body = $('body'),
                $select = $(select),
                $options = $select.find('option'),
                $ul = $('<ul></ul>');

            // add the id & classes the new UL
            $ul.addClass('ul-from-select');
            $ul.prop('id', $select.prop('id') + '_ul');

            // add data for 2-way binding
            $ul.data('bind', $select.prop('id'));
            $select.data('bind', $ul.prop('id'));

            // add the select options to the list
            $.each($options, function(i, option) {
                var $li = $('<li></li>');

                // Add the original text
                $li.text($(option).text());

                // check if it's selected
                ($(option).is(':selected') || ($(option).attr('selected') == 'selected'))
                    ? $li
                        .addClass('active-select')
                        .data('selected', 'selected')
                    : true;

                //add it to the unordered list
                $ul.append($li);
            });

            var $li = $ul.children('li');

            // handler for option click
            $li.click(function() {

                var $this = $(this),
                   $dataSelected = $this.data('selected'),
                   $select = $('#' + $this.parent().data('bind')),
                   $option = $select.find('option').eq($this.index()),
                   newState = ($dataSelected) ? 'unselected' : 'selected';

                // toggle the active/inactive state
                (newState == 'selected')
                    ? $this
                        .addClass('active-select')
                        .data('selected', 'selected')
                    : $this
                        .removeClass('active-select')
                        .removeData('selected');

                // mimic the action on the actual select
                (newState == 'selected')
                    ? $option.prop('selected', 'selected')
                    : $option.removeProp('selected');

                // trigger a custom event
                $this.trigger('SelectToUl.toggle');
            });

            // // handler for original <select> option change
            // // just in case some1 tweaks that
            // $options.change(function() { console.log('yolo');
            //     var $this = $(this),
            //         $ul = $('#' + this.closest('select').data('bind')),
            //         $li = $ul.children('li').eq($this.index()),
            //         newState = ($this.attr('selected') == 'selected') ? 'selected' : 'unselected';
            //
            //     (newState == 'selected')
            //         ? $li
            //             .addClass('active-select')
            //             .data('selected', 'selected')
            //         : $li
            //             .removeClass('active-select')
            //             .removeData('selected');
            // });

            // hide the original <select>
            $select.hide();
            // add the unordered list after the select
            $select.after($ul);

            return $(select)
        }

        function destroy(select) {
            var $select = $(select),
                $ul = $('ul').filter(function() {
                    return ($(this).data('bind') == $select.prop('id'))
                });
            
            // cancel the handlers
            $ul.find('li').off('click');
            // remove the element
            $ul.remove();
            return $(select)
        }


        return this.each(function() {
            if (option == 'destroy')
                destroy(this);
            else
                createUlFromSelect(this)
        });
    }
}( jQuery ));