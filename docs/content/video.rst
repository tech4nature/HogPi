*****
Video
*****

.. contents:: Table of Contents


Configuring a Raspberry Pi Camera to Work with FFMPEG
=====================================================

To cofigure a Raspberry Pi Camera or other MMAL based Pi Camera to be useable in FFMPEG run this command:

.. code-block:: bash

  sudo modprobe bcm2835-v4l2

After running this command the camera will be accessible at /dev/video0

Example FFMPEG code:

.. code-block:: bash

  ffmpeg -f v4l2 -r 25 -video_size 1280x720 -pixel_format yuv422p -input_format h264 -i /dev/video0 -c:v copy -t 30 test.mp4

Record a 30 second long video with the resolution of 1280 by 720 and writes to test.mp4
