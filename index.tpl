<html>
<head>
    <title>PiCam</title>
    <link rel="stylesheet" href="static/bootstrap.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
</head>
<body>
<div class="container" style='margin-top:20px'>
<p>
    %if raspivid:
        <a class='btn btn-success' href="rtsp://{{ip}}:9000/">Show the Preview!</a>
    %else:
        <a class='btn btn-warning' href="/video">Start Video</a>
    %end
</p>
<p>
    %if raspistill:
        <a class='btn btn-danger' href="/stopTimelapse">Stop the timelapse</a>
    %else:
        <a class='btn btn-primary' href="/startTimelapse">Start the timelapse</a>
    %end
</p>
    <img width=480 height="270" alt="Latest shot" src="/static/latest.jpg"/>
</div>
</body>
</html>
