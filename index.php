<html>
 <head>
<meta http-equiv="refresh" content="50">
  <h1>Environment Monitor at DC1-University Villa</h1>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <script type="text/javascript">
    google.charts.load('current', {'packages':['gauge']});
    google.charts.setOnLoadCallback(drawGauge);

    var gaugeOptions = {min: 0, max: 100, yellowFrom: 75, yellowTo: 90,
      redFrom: 91, redTo: 100, minorTicks: 5, greenFrom: 35, greenTo: 74,animation:{
          duration: 4000,
          easing: 'inAndOut',
        }
       };
    var gauge;

    <?php

	$cel = rtrim(file_get_contents("/home/pi/temp-data.txt"));
	    $f = ($cel * 9/5) + 32;

?>
    function drawGauge() {
      gaugeData = new google.visualization.DataTable();
      gaugeData.addColumn('number', 'Temperature');
      gaugeData.addColumn('number', 'Humidity');
      gaugeData.addRows(2);
      gaugeData.setCell(0, 0, 0);
      gaugeData.setCell(0, 1, 0);
      gauge = new google.visualization.Gauge(document.getElementById('gauge_div'));
      gauge.draw(gaugeData, gaugeOptions);

    }

      setTimeout (function() {
      gaugeData = new google.visualization.DataTable();
      gaugeData.addColumn('number', 'Temperature');
      gaugeData.addColumn('number', 'Humidity');
      gaugeData.addRows(2);
      gaugeData.setCell(0, 0, <?php echo $f; ?>);
      gaugeData.setCell(0, 1, <?php echo rtrim(file_get_contents("/home/pi/humi-data.txt")); ?>);
      gauge.draw(gaugeData, gaugeOptions);
    }, 200);


  </script>
 </head>
 <body>
  <div id="gauge_div" style="width:560px; height: 280px;"></div>
 </body>
</html>

