#!/usr/bin/env python

# picam.py
# Really handy to serve and configure raspberry + picam as timelapse camera

from bottle import route, run, debug, template, redirect, os, time, static_file


@route('/')
def index():
    ip = os.popen('hostname -I').read().split()[0].strip()
    raspivid = os.popen('pgrep raspivid').read() != ''
    raspistill = os.popen('pgrep raspistill').read() != ''
    return template('index', raspivid=raspivid, raspistill=raspistill, ip=ip)

@route('/static/<path:path>')
def latest(path):
    print path
    return static_file(path, './')

def startVideo():
    os.system("raspivid -n -w 1280 -h 720 -b 4500000 -fps 30 -t 0 -o - | cvlc -I dummy -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:9000/}' :demux=h264 &")

def stopVideo():
    os.system('killall vlc')
    os.system('killall raspivid')

def startTimelapse():
    path = "/media/sandisk/timelapses/" + time.strftime('%Y-%m-%d')
    if not os.path.exists(path):
        os.mkdir(path)
    os.system("raspistill -w 1920 -h 1080 -o " + path + r"/%05d.jpg -tl 5000 -t 84700000 -l latest.jpg &")

def stopTimelapse():
    os.system('killall raspistill')

@route('/video')
def video():
    stopTimelapse()
    startVideo()
    redirect('/')

@route('/startTimelapse')
def start():
    stopVideo()
    startTimelapse()
    redirect('/')

@route('/stopTimelapse')
def stop():
    stopTimelapse()
    redirect('/')

debug(True)
run(reloader=True, host="0.0.0.0", port=8000)
