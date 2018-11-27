import io
import time
import picamera
from base_camera import BaseCamera


class Camera(BaseCamera):


    @staticmethod
    def frames(resolution, framerate):
        with picamera.PiCamera() as camera:
            camera.resolution = resolution
            camera.framerate = framerate
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

    def change_configuration(self, res_x, res_y, framerate):
        self.change_lock()
        while self.thread is not None:
            continue
        self.change_lock()
        print("change configuration")
        self.change_resolution(int(res_x), int(res_y))
        self.change_frame_rate(framerate)
        BaseCamera.__init__(self)




