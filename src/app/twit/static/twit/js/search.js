$(document).ready(function(){
    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // The api back to use
    var engine = 'Lucene';

    var do_display = false;

    $('.adv-modal-submit').click(function(e){

        /*this is to pop advance search modal*/
         e.preventDefault();
         console.log('an advance search was made')
         console.log($('.cities').val());
         console.log($('.states').val());

        /*call advance search Api*/
        searchLuceneAdvance();
    });


    $('.adv-search').click(function(e){

        /*this is to pop advance search modal*/
        e.preventDefault();
        console.log('this is advance search. pop modal');
         $('#mapid').css( "display","none" );
         $('.date-inp-range-adv').daterangepicker();
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
      if(!do_display){
              $('#mapid').css( "display","block");
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
        if(!do_display){
              $('#mapid').css( "display","block");
        }



      }
    }

    function displayData(data){
        $("#display-d").empty();
        var result = '';
        console.log('DOINg display');
        for(i in data){
            result+="User: "+ data[i].user.screen_name + "; Relevance : "+ data[i].rank+" <br> &emsp; Tweeted: "+data[i].text+"<br><hr><br>";
        }
        $("#display-d").html(result);
    }

    function searchLuceneBasic(query_str){

        var url = "/api/lucene/?query="+ query_str

        $.ajax({
            url: url,
            type:'GET',
            success: function(data){
               console.log(data['results']);
               modal.style.display = "none";

               if(do_display){
                    displayData(data['results']);
               }
               else{
                   //call map here to generate tweet with cooardinates
                   //IAN CALL YOUR MAPPER FUNCTION HERE
                   //PASS data['results'] ot it. its an array of dict

                    $('#mapid').css( "display","block" );
               }

            }
        });

        /*clear modal*/
        $('#search-adv').trigger('reset');
    }

    function searchLuceneAdvance(){
                /*call advance search Api*/
        $.ajax({
            url: "/api/advance/lucene/",
            type:'GET',
            data:{
                'and': $('#search-input-adv-and').val(),
                'or': $('#search-input-adv-or').val(),
                'not': $('#search-input-adv-not').val(),
                'date_range': $('.date-inp-range-adv').val(),
                'city': $('.cities').val(),
                'state': $('.states').val(),
                'hashtags': $('.coord-tag-adv').val()
            },
            success: function(data){
            modal.style.display = "none";
             if(do_display){
                    displayData(data['results']);
             }
             else{
                   console.log(data);
                   //call map here to generate tweet with cooardinates
                   //IAN CALL YOUR MAPPER FUNCTION HERE
                   //PASS data['results'] to it. its an array of dict

                $('#mapid').css( "display","block" );
             }
            }
        });

        /*clear modal*/
        $('#search-adv').trigger('reset');

    }

    $('.map-or-display').click(function(){
            if($(this).prop("checked") == false){
                $('#mapid').css( "display","none" );
                do_display = true;
            }
            else if($(this).prop("checked") == true){
                $('#mapid').css( "display","block" );
                do_display = false;
            }
    });

});
