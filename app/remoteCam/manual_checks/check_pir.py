import pir

# ========================
# class set up
# ==========================
pir_sensor = pir.sensor()
# ==========================
# functions
# ==========================
# transfers and deletes all mp4 videos
def transfer_video():

    with pysftp.Connection("192.168.4.1", username="pi", password="hog1hog1") as sftp:
        for item in video_dir:
            if item.endswith(".mp4"):
                sftp.chdir(video_path)  # temporarily chdir to allcode
                print(sftp.put(video_path + item, confirm=True))
                os.remove(os.path.join(video_path, item))
                print("Complete")  # upload file to allcode/pycode on remote


# ==========================
# Main program
# ==========================
if __name__ == "__main__":
    while True:
        a = pir_sensor.read(4)
        print(a)
        if a == 1:
            print("pir on")
        else:
            print("pir off")
