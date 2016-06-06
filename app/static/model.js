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

  // Put the results in a div
  // posting.done(function( data ) {
  //   var content = $( data ).find( "#content" );
  //   $( "#result" ).empty().append( content );
  // });
});