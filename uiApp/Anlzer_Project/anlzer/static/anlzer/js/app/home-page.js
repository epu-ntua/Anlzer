/**
 * Created by DarkA_000 on 4/6/2016.
 */

/* JS responsible for the behaviour of the project drawer */
$(document).ready(function() {
    var $body = $('body'),
        $toggleElement = $('.toggle-project-drawer'),
        $projectDrawer = $('.project-drawer'),
        $closeDrawer = $('.drawer-close');
    
    /* toggle it on button "View Projects" click */
    $toggleElement.on('click', function(e) {
        e.stopPropagation();
        $projectDrawer.toggleClass('open');
        $toggleElement.toggleClass('active');
    });
    
    /* close it when anywhere in the body is clicked */
    $body.on('click', function() {
        $projectDrawer.removeClass('open');
        $toggleElement.removeClass('active');
    });

    /* close in on "X" click */
    $closeDrawer.on('click', function() {
        $projectDrawer.removeClass('open');
        $toggleElement.removeClass('active');
    });

    /* stop propagation of events inside project drawer so the click
     * doesnt propagate to the 'body' and thus close the drawer
     */
    $projectDrawer.on('click', function(e) {
        e.stopImmediatePropagation();
        e.stopPropagation();
    })
});