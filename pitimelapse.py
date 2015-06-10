#!/usr/bin/env python

# picam.py
# Really handy to serve and configure raspberry + picam as timelapse camera

from bottle import route, run, debug, template, redirect, os, time, static_file
import subprocess


@route('/')
def index():
    values = dict(raspivid=os.popen('pgrep raspivid').read() != '')
    values["raspistill"] = os.popen('pgrep raspistill').read() != ''
    values["ip"] = os.popen('hostname -I').read().split()[0].strip()
    values["time"] = time.asctime()
    values["usage"] = subprocess.Popen(
        ['df', '/media/sandisk'], stdout=subprocess.PIPE).communicate()[0].split('\n')[1].split()[4]
    return template('index', **values)


@route('/static/<path:path>')
def latest(path):
    return static_file(path, './')


def startVideo():
    os.system(
        "sudo -u pi raspivid -n -w 1280 -h 720 -b 4500000 -fps 30 -t 0 -o - "
        "|sudo -u pi vlc-wrapper -I dummy -vvv stream:///dev/stdin --sout "
        "'#rtp{sdp=rtsp://:9000/}' :demux=h264 &")


def stopVideo():
    os.system('killall vlc')
    os.system('killall raspivid')


def startTimelapse():
    path = "/media/sandisk/timelapses/" + time.strftime('%Y-%m-%d')
    if not os.path.exists(path):
        os.mkdir(path)
    os.system("raspistill -w 1920 -h 1080 -o " + path +
              r"/%05d.jpg -tl 5000 -t 84700000 -l "
              "/home/pi/pitimelapse/latest.jpg &")


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


@route("/setTime/<newTime>")
def setTime(newTime):
    os.system("sudo date -s %s &" % newTime)

debug(True)
run(reloader=True, host="0.0.0.0", port=8000)
