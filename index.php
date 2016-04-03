<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="css/login.css">
        <link rel="stylesheet" href="css/search.css">
        <link rel="stylesheet" href="css/bootstrap.min.css">
        <script src="js/jquery.min.js"></script>
        <script src="js/bootstrap.min.js"></script>
        <title>Scavenger Search</title>
    </head>
    <body>
        <div class="container">            
        <div class="row">
            <h1>Scavenger Search</h1>
        </div>
        <div class="row">
            <h2>The best of its kind!</h2>
            <div class="col-md-12">
                <div id="custom-search-input">
                    <div class="input-group col-md-12">
                        <input name="search" type="text" class="form-control input-lg" placeholder="Search"  onkeyUp="searchq(1,1)" />
                        <span class="input-group-btn">
                            <button class="btn btn-info btn-lg" type="button">
                                <i class="glyphicon glyphicon-search"></i>
                            </button>
                        </span>
                    </div>
                </div>
            </div>
            
            <label class="radio-inline">
              <input id="radioEverything" checked="checked" onclick="searchq(1,1);" type="radio" name="searchType">Everything
            </label>
            <label class="radio-inline">
              <input id="radioPDF" onclick="searchq(1,1);" type="radio" name="searchType">PDFs only
            </label>
            
<!--
            <div class="col-md-4">
                <div class="form-group">
                  <input type="text" class="form-control" placeholder="number of results">
                </div>
            </div>
-->
        </div>
        <div class="row">
            <div class="col-md-12">
                <div id="output">
                    <h3>Enter the search query to get the results</h3>
                </div>
            </div>
        </div>
    </div>
    
    <script type="text/javascript">

      function searchq (pageNo,isCorrect){
          var searchTxt= $("input[name='search']").val();
          var checked=0;
          if($("#radioEverything").is(':checked')){
            checked=0;
          } else if($("#radioPDF").is(':checked')){
            checked=1;
          }
          
          if(isCorrect != '1'){
            searchTxt = $("#SuggestedText");
          }

          $.get("engine.php", {search:searchTxt,page:pageNo,radio:checked,isCorrected:isCorrect}, function(output){
                $("#output").html(output)
            });
          //To get suggestions run it on another python file :P
//          $.get("suggestions.php", {search:searchTxt}){
//              $("input[name='search']").attr("typeahead","hello, just testing");
//          });
      }

      function searchw (pageNo, isCorrect) {
        var searchTxt= $("input[name='search']").val();
          var checked=0;
          if($("#radioEverything").is(':checked')){
            checked=0;
          } else if($("#radioPDF").is(':checked')){
            checked=1;
          }

          $.get("wrong_engine.php", {search:searchTxt,page:pageNo,radio:checked,isCorrected:isCorrect}, function(output){
                $("#output").html(output)
            });
      }
        //if(isCorrected=="false"){

        //}
        $(document).ready(function(){
            $('[data-toggle="tooltip"]').tooltip(); 
        });
    </script>
        
    </body>
</html>