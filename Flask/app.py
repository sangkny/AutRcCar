from importlib import import_module
import os
from flask import Flask, render_template, Response
import gpioController as g

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera

app = Flask(__name__,template_folder='Templates')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(Camera):
    """Video streaming generator function."""
    while True:
        frame = Camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
