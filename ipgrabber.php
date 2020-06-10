<?php
  echo "A patetic ip logger in php.. yeah.. that's right dude... I know..";
	$ip = $_SERVER['REMOTE_ADDR'];
	$browser = $_SERVER['HTTP_USER_AGENT'];
	$dateTime = date('Y/m/d G:i:s');
	$file = "ip.html";
	$file = fopen($file, "a");
	$data = "<pre><b>User IP</b>: $ip <br><b>Browser</b>: $browser <br><b>Time: </b>$dateTime <br></pre>";
	fwrite($file, $data);
	fclose($file);
?> 
