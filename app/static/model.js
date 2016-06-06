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

// $("#formsurvey").submit(function(event) {
//
//   // Stop form from submitting normally
//   event.preventDefault();
//
//   // Get some values from elements on the page:
//   var $form = $( this ),
//       data = {},
//       keys = [];
//   var answers = [];
//   $("#formsurvey").find("input").each(function(){ keys.push(this.id); });
//   for (key_ in keys)
//       answers.push({quesiton_id: key_, answer: $form.find( "input "+ key).val()});
//   data.answers = answers;
//   // user = $form.find( "input " + key ).val(),
//   // password = $form.find("input[name='password']").val(),
//   url = $form.attr( "action" );
//
//   // Send the data using post
//   var posting = $.post( url, data );
//
//   // Put the results in a div
//   // posting.done(function( data ) {
//   //   var content = $( data ).find( "#content" );
//   //   $( "#result" ).empty().append( content );
//   // });
// });