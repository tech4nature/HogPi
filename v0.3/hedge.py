import post
import thermo
import video
import weight

camera = video.ffmpeg

camera.__init__()
camera.record("1stPASS.mp4", 10, True)
camera.extract_time(True)
camera.sync_av("2ndPASS.mp4", True)
camera.BITC_flip("3rdPASS.mp4", True)
