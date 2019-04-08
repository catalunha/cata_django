<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" type="text/css" href="../estilos.css">
  	<link rel="StyleSheet" href="../dtree/dtree.css" type="text/css" />
  	<script type="text/javascript" src="../dtree/dtree.js"></script>
    
    <title>Ação </title>
  </head>
 
<body>
  <?php
    if(isset($_POST['nivel'])){
      echo "POST: ".$_POST['nivel'];
    }else{
      echo "POST Nada";
    }
    if(isset($_GET['a'])){
      echo "GET: ".$_GET['a'];
    }else{
      echo "GET Nada";
    }
?>
  </body>
</html>
