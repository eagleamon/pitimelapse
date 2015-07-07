#!/usr/bin/env python

# pitimelapse.py
# Really handy to serve and configure raspberry + picam as timelapse camera

from bottle import route, run, debug, template, redirect, os, time, static_file
import subprocess

USBPATH = '/media/usb/'

@route('/')
def index():
    values = dict(video=os.popen('pgrep raspivid').read() != '')
    values["raspistill"] = os.popen('pgrep raspistill').read() != ''
    values["ip"] = os.popen('hostname -I').read().split()[0].strip()
    values["time"] = time.asctime()
    values["usage"] = subprocess.Popen(
        ['df', USBPATH], stdout=subprocess.PIPE).communicate()[0].split('\n')[1].split()[4]
    return template('index', **values)


@route('/static/<path:path>')
def latest(path):
    return static_file(path, './')


def startVideo():
    os.system(
        "sudo -u pi raspivid -n -w 1280 -h 720 -b 4500000 -fps 30 -t 0 -o - "
        "|sudo -u pi vlc-wrapper -I dummy -vvv stream:///dev/stdin :live-caching=0 --sout-rtp-caching 100 --sout "
        "'#rtp{sdp=rtsp://:8554/}' :demux=h264 :rtsp-caching=50 :sout-mux-caching=10 &")

def startVideo2():
    os.system('sudo -u pi h264_v4l2_rtspserver -W 1280 -H 720')

def stopVideo():
    os.system('killall vlc')
    os.system('killall raspivid')

def stopVideo2():
    os.system('killall -9 h264_v4l2_rtspserver')

def startTimelapse():
    path = USBPATH + "timelapses/" + time.strftime('%Y-%m-%d')
    if not os.path.exists(path):
        os.makedirs(path)
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

@route('/unmount')
def unmount():
    os.system('pumount %s' % USBPATH)

@route('/stopTimelapse')
def stop():
    stopTimelapse()
    redirect('/')


@route("/setTime/<newTime>")
def setTime(newTime):
    os.system("sudo date -s %s &" % newTime)

debug(True)
run(reloader=True, host="0.0.0.0", port=8000)
