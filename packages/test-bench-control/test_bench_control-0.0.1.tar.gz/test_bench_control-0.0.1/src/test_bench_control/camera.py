from picamera2 import Picamera2

def take_picture(path,pic_name):
    complete_path=str(path)+"/"+str(pic_name)
    picam2=Picamera2()
    picam2.start_and_capture_file(complete_path,show_preview=False)