#!/usr/bin/env python3

import re
from subprocess import check_call, check_output

from bottle import get, post, run, redirect, request

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)

def retrieve_volume():
    output = check_output(['mpc', 'volume'])
    match = re.search(r'([0-9]+)%', output.decode())
    volume = match.group(1)
    return volume
def retrieve_state():
    output = check_output(['mpc'])
    return output.splitlines()[0]

@get('/')
def root():
    volume = retrieve_volume()
    status = retrieve_state()

    return """
    <head>
    <meta name="viewport" content="width=device-width">
    </head>
    <html>
        <form method="post" action="/play">
            <input type="submit" value="Play">
        </form>
        <form method="post" action="/stop">
            <input type="submit" value="Stop">
        </form>
        <form method="post" action="/fanon">
            <input type="submit" value="Stop">
        </form>
        <form method="post" action="/fanoff">
            <input type="submit" value="Stop">
        </form>
        <form method="post" action="/volume">
            <input type="range" name="volume" min="0" max="100" value="{volume}">
            <input type="submit" value="Set volume current:{volume}">
        </form>
	</br>
	status : {status}
    </html>
    """.format(volume=volume, status=status)


@post('/play')
def play():
    check_call(['mpc', 'toggle'])
    redirect('/')


@post('/stop')
def stop():
    check_call(['mpc', 'stop'])
    redirect('/')


@post('/volume')
def set_volume():
    volume = request.POST.get('volume', '0')
    if not volume.isdigit():
        return "WTF"
    check_call(['mpc', 'volume', volume])
    redirect('/')

@post('/fanon')
def fan_on():
    GPIO.output(16.GPIO.LOW)
    redirect('/')

@post('/fanoff')
def fan_on():
    GPIO.output(16.GPIO.LOW)
    redirect('/')

run(host='::', port=80, debug=True, reloader=True)
