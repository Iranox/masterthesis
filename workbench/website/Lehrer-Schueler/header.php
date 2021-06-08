<?php

function myHeader() {
  return '
<!DOCTYPE html>
<html>

<head>
  <title>Projekt "Lehrer-Schüler-Beziehung"</title>
  <meta name="description" content="website description" />
  <meta name="keywords" content="website keywords, website keywords" />
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta charset="ISO-8859-1" />
  <link rel="stylesheet" type="text/css" href="css/style.css" />
  <!-- modernizr enables HTML5 elements and feature detects -->
  <script type="text/javascript" src="js/modernizr-1.5.min.js"></script>
</head>

<body>
  <div id="main">

    <header>
      <div id="strapline">
  <div id="welcome_slogan">
    <h1 align="center">Lehrer-Schüler-Beziehung</h1>
  </div><!--close welcome_slogan-->
      </div><!--close strapline-->
      <nav>
  <div id="menubar">
          <ul id="nav">
            <li><a href="index.php">Projekt</a></li>
            <li><a href="data.php">Data</a></li>
            <li><a href="prototyp.php">Prototyp</a></li>
          </ul>
        </div><!--close menubar-->
      </nav>
    </header>
    <div id="site_content">
      <div id="content">
        <div class="content_item">
';
}
