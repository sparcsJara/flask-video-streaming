#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import time

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

camera = Camera()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/config', methods = ['POST'])
def config_change():
    if request.method == 'POST':
        try:
            frame_rate = request.form.get('frame_rate')
            resolution_x = request.form.get('resolution_x')
            resolution_y = request.form.get('resolution_y')
            camNum = request.form.get('camNum')
            print("camNum:" + camNum +", time:"+str(time.time()))
            camera.change_configuration(resolution_x, resolution_y, frame_rate)
            # cv2.imwrite(os.pathfind .join(path, "img", name), image)
            # wriitenToDir = HomeSurveillance.add_face(name, image, upload=True)
            message = "file uploaded successfully"
        except Exception as e:
            print(e)
            message = "file upload unsuccessfull"
        return Response(message)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, threaded=True)
