<html>
<head>
    <title>PiTimelapse</title>
    <link rel="stylesheet" href="static/bootstrap.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <script>
        function sendTime(){
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open("GET", "/setTime/" + new Date().toISOString(), false);
            xmlHttp.send(null);
            location.reload()
        }
    </script>
</head>
<body>
<div class="container" style='margin-top:20px'>
    <p>
    <span>
        %if video:
            <a class='btn btn-success' href="rtsp://{{ip}}:8554/">Show the Preview!</a>
        %else:
            <a class='btn btn-warning' href="/video">Start Video</a>
        %end
    </span>
    <span>
        %if raspistill:
            <a class='btn btn-danger' href="/stopTimelapse">Stop the timelapse</a>
        %else:
            <a class='btn btn-primary' href="/startTimelapse">Start the timelapse</a>
        %end
    </span>
    <span class='pull-right'><a class='btn btn-danger' href='/unmount'>Unmount</a></span>
    </p>
    <img class='img-thumbnail' alt="Latest shot" src="/static/latest.jpg">
    <p>
        Actual time: {{time}}
        <a class='btn btn-small' href='javascript:sendTime()'>Set time from browser</a>
        <span class="pull-right">{{usage}}</span>
    </p>
</div>
</body>
</html>
