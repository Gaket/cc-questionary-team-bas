/**
 * Created by Bulat on 31.05.2016.
 */

$("#loginform").submit(function(event) {

  // Stop form from submitting normally
  event.preventDefault();

  // Get some values from elements on the page:
  var $form = $( this ),
    user = $form.find( "input[name='user']" ).val(),
    password = $form.find("input[name='password']").val(),
    url = $form.attr( "action" );

  // Send the data using post
  var posting = $.post( url, { user: user, password: password } );
});


$(document).ready(function(){

  $("[type=range]").each(function () {
    var newval=$(this).val(),
        cls = $(this).attr("class");
    $("span." + cls).text(newval)
  });
  var ran = $("[type=range]");
  ran.on("change mousemove", function(){
    var newval=$(this).val(),
        cls = $(this).attr("class");
    $("span." + cls).text(newval);
  });
});