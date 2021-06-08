<?php
require_once("header.php");
require_once("footer.php");
set_include_path(get_include_path() . PATH_SEPARATOR .  'easyrdf-0.9.0/lib/');
require_once "EasyRdf.php";

function get_lehrername($name, $client){
   $result = $client->query("select distinct ?nachname where {<http://hmt-leipzig.de/Data/Person/L.".$name.">  foaf:lastname ?nachname.}");
   foreach ($result as $r) {
     return $r->nachname;
   }
}
    $ENDPOINT = 'http://localhost:1983/sparql/';
    $sparql = new EasyRdf_Sparql_Client($ENDPOINT);
    $result = $sparql->query("select distinct  ?leherid  ?name where{?s a
                             <http://www.w3.org/2002/07/owl#Observation>;
                            <http://hmt-leipzig.de/Data/Model#Lehrer> ?leherid .
                            ?leherid foaf:lastname ?name} ORDER BY ?name");
 $lehrerauswahl = "<style type=\"text/css\">#mynetwork {width: 600px;height: 600px;}
                  </style><h2 align='center'>Prototyp zur Visualierung</h2>
                  <p>Dies ist ein Prototyp zur Visualisuerng der RDF-Daten.
                  Dabei werden die Lehrer und irgend entsprechenden Schüler als
                  Graph dargestellt. </p> <div id=\"text\">
                  <form action=\"prototyp_lehrer.php\" method=\"get\">
                  <select name=\"name\">";
   foreach ($result as $r) {
        $lehrerauswahl = $lehrerauswahl."<option value=\"".str_replace("http://hmt-leipzig.de/Data/Person/L.", "" ,$r->leherid);
        $lehrerauswahl = $lehrerauswahl."\">".$r->name."</option>";
   }
   $lehrerauswahl = $lehrerauswahl."</select> <br/> <input type=\"submit\" /></form></div>";


   if (isset($_GET["name"])){
     $lehrerauswahl = $lehrerauswahl."<script src=\"https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js\"></script>";
     $result = $sparql->query("select distinct  ?schueler where {?s <http://hmt-leipzig.de/Data/Model#Lehrer> <http://hmt-leipzig.de/Data/Person/L.".$_GET["name"].">; <http://hmt-leipzig.de/Data/Model#Schueler> ?schueler.}");
     $lehrerauswahl = $lehrerauswahl."<div><h3> Name des Lehrers: " .get_lehrername($_GET["name"], $sparql). "</h3>";
     $lehrerauswahl = $lehrerauswahl."<br/>Anzahl der Schühler: ".count($result);
     $anzahl_der_facher = $sparql->query("select distinct ?fach where {?s <http://hmt-leipzig.de/Data/Model#Lehrer> <http://hmt-leipzig.de/Data/Person/L.".$_GET["name"].">; <http://hmt-leipzig.de/Data/Model#Fach> ?fach.}");
     $f = "";
     foreach ($anzahl_der_facher as $facher) {
              $f = $f." ".str_replace("@de","",$facher->fach);
     }
     $lehrerauswahl = $lehrerauswahl."<br/> Fächer: ".$f."<br/>";
     $kollegen="";
     foreach ($result as $r) {
       $l = $sparql->query("select distinct ?lehrer where {?s <http://hmt-leipzig.de/Data/Model#Schueler> <".$r->schueler.">;  <http://hmt-leipzig.de/Data/Model#Lehrer> ?lehrer.}");
       foreach ($l as $lehrer_name) {
         if(strpos($lehrer_name->lehrer, $_GET["name"]) === false){
           $kollegen = $kollegen.get_lehrername(str_replace("http://hmt-leipzig.de/Data/Person/L.", "",$lehrer_name->lehrer), $sparql).", ";
         }
       }
     }
     $lehrerauswahl = $lehrerauswahl."Kollegen: ".implode(', ',array_unique(explode(', ', $kollegen)))."<br/>";^M
     $lehrerauswahl = $lehrerauswahl."</div>";
     $lehrerauswahl = $lehrerauswahl.'<div id="mynetwork" />';
     $node = "{id:1, label:'".get_lehrername($_GET["name"], $sparql)."'},";
     $egdes = "";
     $index=2;
     foreach ($result as $r) {
       $schueler = $r->schueler;
       $node = $node."{id:".$index.", label:'".$schueler."'},";
       $egdes = $egdes."{from: 1, to: ".$index."},";
       $index++;
     }
     $lehrerauswahl = $lehrerauswahl.$egdes.$node;
     $draw_graph = "var container = document.getElementById('mynetwork');
                    var data = { nodes: nodes,edges: edges};var options = {};
                    var network = new vis.Network(container, data, options);</script>";
     $graph = "<script>var nodes = new vis.DataSet([".$node."]);var edges = new vis.DataSet([".$egdes."]);".$draw_graph;
     $lehrerauswahl = $lehrerauswahl."<br/>";
     $lehrerauswahl = $lehrerauswahl.$graph;
   }

   echo(myHeader().($lehrerauswahl).myFooter());
?>
