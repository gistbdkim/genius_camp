from picamera2 import Picamera2
picam2 = Picamera2()

while True:
    picam2.start_and_capture_file("test.jpg", delay=0.1, show_preview=False)