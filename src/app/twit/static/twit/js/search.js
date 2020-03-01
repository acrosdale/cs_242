$(document).ready(function(){

   /*$("button").click(function(){
    $.ajax({
        url: "demo_test.txt",
        success: function(result){
            $("#div1").html(result);
        }
    });

  });*/

  $('.switch-input').click(function(){

    console.log($(this).val());
  });

  $('.search-bar').click(function(e){
        e.preventDefault();
        console.log('form stopped');
  });



});