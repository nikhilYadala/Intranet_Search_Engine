<?php
  if(isset($_GET['search']) && isset($_GET['page']) && isset($_GET['radio'])){
        if($_GET['search'] != ""){
          if($_GET['isCorrected'] == '1') {
            switch($_GET['radio']){
                case 0:
                    $path = "wrongQuery_searcher.py";
                    break;
                case 1:
                    $path = "wrongQuery_pdf_searcher.py";
                    break;
            }
          } else {
            switch($_GET['radio']){
                case 0:
                    $path = "wrongQuery_searcher.py";
                    break;
                case 1:
                    $path = "wrongQuery_pdf_searcher.py";
                    break;
            }
          }
          // shell_exec("chmod 777 *");
           // $command = escapeshellcmd('python '.$path.' '.str_replace(' ','{}',$_GET['search']).' > files.txt');
           $output = shell_exec('python '.$path.' '.str_replace(' ','{}',$_GET['search']).' 2>&1');
           // var_dump($output);
           // $output = file_get_contents('files.txt');
          
          $arr = explode("\n", $output);
          // var_dump($output);
          $didYouMean = "";
          if(strpos($arr[0], '<') !== false){
            $noOfResults = (count($arr)-1)/2;
            $stop = 10*$_GET['page'];
            $start = $stop - 9;
            $searchTime = substr($arr[0],-18,-2);
            if($searchTime[0] == '='){
              $searchTime = substr($searchTime, 1);
            }
            $noOfResults = floor($noOfResults);
            if($stop > $noOfResults) {
                $stop = $noOfResults;
            }
         } else {
            $noOfResults = (count($arr)-2)/2;
            $didYouMean = $arr[0];
            $stop = 10*$_GET['page']+1; 
            $start = $stop - 9;
            $searchTime = substr($arr[1],-18,-2);
            if($searchTime[0] == '='){
              $searchTime = substr($searchTime, 1);
            }
            $noOfResults = floor($noOfResults);
            if($stop > $noOfResults) {
                $stop = $noOfResults;
            }
            echo '<div class="alert alert-info">
                <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
              Showing results for <strong>'.$didYouMean.'</strong>. Search for <strong id="SuggestedText"><a href="#" onclick="searchw(1,5)">'.$_GET['search'].'</a></strong> instead.
            </div>';
         }

         echo '<p>Showing top '.$noOfResults.' results! Search time: '.$searchTime;

         // var_dump($start);
              
            //Change this to get the top results and search time
              
            for ($i=$start;$i<=$stop;$i++) {
                $link = $arr[2*$i-$start];
                //Title would be in bold and the description would be inside the href. On clicking the title it should redirect to the link. The link can come as a tooltip

                $title = $link;
                $description = $arr[2*$i-$start+1];
                echo '<li class="list-group-item"><a href="'.$link.'" data-toggle="tooltip" title="Hooray!"><p><b>'.$title.'</b></p></a><p>'.$description.'</p></li>';
            }
              echo '<ul class="pagination">';

              if($noOfResults%10 == 0) {
                  $stop = $noOfResults/10;
              } else {
                  $stop = $noOfResults/10+1;
              }
              for($i=1;$i<=$stop;$i++){
                  if($i == $_GET['page']){
                      $active = 'class="active" ';
                  } else {
                      $active = "";
                  }
                  echo '<li '.$active.'onclick="searchw('.$i.',1)"><a href="#">'.$i.'</a></li>';
              }
              echo '</ul>';
      }else{
        echo '<h3>Enter the search query to get the results</h3>';    
      }
  } else {
      echo '<h3>Enter the search query to get the results</h3>';
  }
?>