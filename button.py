import RPi.GPIO as GPIO
import time
import alsaaudio
import mpd

client = mpd.MPDClient()
client.connect("localhost", 6600)

mixer = alsaaudio.Mixer("Speaker")
GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(26)
    if input_state == False:
	vol = mixer.getvolume()[0]
	vol += 5
	print(vol)
	if vol <= 100:
            mixer.setvolume(vol)
	    print(vol)
	else :
	    print("volume is at maximum")
	time.sleep(0.2)

    input_state = GPIO.input(16)
    if input_state == False:
	vol = mixer.getvolume()[0]
	vol -= 5
	print(vol)
	if vol < 0:
	    vol = 0
        mixer.setvolume(vol)
	print(vol)
	time.sleep(0.2)

    input_state = GPIO.input(20)
    if input_state == False:
	if client.status()["state"] == "play":
	    client.stop()
	else :
	    client.play()

	time.sleep(0.2)
