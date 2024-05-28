from picamera import PiCamera
import time
camera = PiCamera()
time.sleep(0.5)
camera.resolution = (1920, 1080)
camera.vflip = True
camera.contrast = 10
camera.framerate = 30
file_name = "/home/pi/Pictures/video_" + str(time.time()) + ".h264"
print("Start recording...")
camera.start_recording(file_name)
camera.wait_recording(2)
camera.stop_recording()
print("Done.")
