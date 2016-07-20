 jQuery(document).ready(function($) {

    /* JS code for the little arrow on the bottom right corner that directs to the top of the page */
    $(".gototop").click(function(e){
        e.preventDefault();
        $('html,body').animate({
            scrollTop:$('html').offset().top
        }, 600,'swing');
    });
     /* end of little arrow scroll code */

     /* Responsible for displaying, hiding & removing any kind of message*/
    (function() {
        var $messages = $('.messages');

        $messages.slideDown('slow', function() {
            setTimeout(function () {
                $messages.slideUp('slow', function () {
                    $messages.remove();
                })
            }, 2000)
        })
    })();
    /* end of: messages js code */


    /* Popover Initialization */
    $(function () {
        $('[data-toggle="popover"]').popover()
    });
    /* end of: popover initialization */


    /* Individual actiovation of tabs*/
    $(function () {
        $('.tabs-menu a').click(function (e) {
            e.preventDefault();
            $(this).tab('show')
        })
    });
    /* end of: tabb activations */
     
    /* add custom tab functionality */ 
    $(function() {
        $('body').on('click', '.btn.ui-tab-btn', function(e) {
            e.preventDefault();

            var $this = $(this),
                $siblings = $this.siblings();
            
            $siblings.each(function(i, sibling) {
                var $sibling = $(sibling);

                $sibling.removeClass('active');
                $($sibling.data('tab')).hide();
            });

            $this.addClass('active');
            $($this.data('tab')).show();

        });

        // initialize
        $('.btn.ui-tab-btn.active').trigger('click');
    });
     /* end of custom tab functionality */
    

 });
 
if ($('.wowload').length > 0) {
    var wow = new WOW(
        {
            boxClass: 'wowload',
            animateClass: 'animated',
            offset: 0,
            mobile: true,
            live: true
        }
    );
    wow.init();
};

 
moduleManager.add(function(){if ($('.switchbox').length > 0) $('.switchbox').bootstrapSwitch();});
 moduleManager.add(function(){if ($('.icheck').length > 0) $('.icheck').iCheck({checkboxClass: 'icheckbox_futurico'});});
moduleManager.add(function(){if ($('.anlzer-tokenfield').length > 0) $('.anlzer-tokenfield').tokenfield({minWidth: 227});});
moduleManager.add(inputFocusManager.reset);
moduleManager.add(function(){if ($('.anlzer-daterangepicker').length > 0) $('.anlzer-daterangepicker').daterangepicker({
        'ranges': {
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    })
    .on('apply.daterangepicker', function(ev, picker) {
      var $startDate = $('#id_start_date'),
          $endDate = $('#id_end_date')
    });
});

$(document).ready(function() {
    moduleManager.call();
});
 
$(window).load(function() {
    $('.project-comments-wrapper .comment-list').perfectScrollbar();
    $('.select-to-ul').selectToUl();
});


