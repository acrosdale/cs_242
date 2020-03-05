$(document).ready(function(){
    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // The api back to use
    var engine = 'Lucene';


    $('.adv-search').click(function(e){

        /*this is to pop advance search modal*/
         e.preventDefault();

        console.log('this is advance search. pop modal');
         $('#mapid').css( "display","none" );
        modal.style.display = "block";

    });

    $('.switch-input').click(function(){
        engine = $(this).val();

        console.log('SEARCH ',engine);
    });

    $('.search-bar').on('submit',function(e){
        e.preventDefault();
        console.log('form stopped');
        if(engine == 'Lucene'){
            console.log($('#search-input').val())
            searchLuceneBasic($('#search-input').val())

        }
    });

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
      $('#mapid').css( "display","block" );
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
        $('#mapid').css( "display","block");
      }
    }

    function searchLuceneBasic(query_str){

        var url = "/api/lucene/?query="+ query_str

        $.ajax({
            url: url,
            type:'GET',
            success: function(data){
               console.log(data['results']);
               //call map here to generate tweet with cooardinates
            }
        });
    }


});