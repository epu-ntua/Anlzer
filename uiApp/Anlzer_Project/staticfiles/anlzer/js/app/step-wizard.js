/**
 * Created by DarkA_000 on 4/6/2016.
 */

$(document).ready(function() {
      
    /* This handler is responsible for updating the steps in any form process
    * that has steps in it. It changes the active UI component denoting the step
    */
    var $body = $('body');

    $body.on('click', '.stepwizard .stepwizard-step', function () {
      var $this = $(this),
          $steps = $('.stepwizard').find('.stepwizard-step');

      $steps.children('.wizard-btn').removeClass('active');
      $this.children('.wizard-btn').addClass('active');
    });
    /*
    * End of handler for steps
    */

});