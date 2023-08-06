import os

def take_picture(camera,path,pic_name,further_libcam_settings=""):
    ##########################################################
    #  Pre:     camera = integer [0,1], path = string, pic_name = string, further_libcam_settings = string
    #  Post:
    #  Example: take_picture(0,"/home/raspi/Desktop","my_pic.jpg","--shutter 1000")
    ##########################################################
    complete_path=str(path)+"/"+str(pic_name)
    camera_number=str(camera)
    cmd=f"libcamera-jpeg -o {complete_path} --nopreview --camera {camera_number} {further_libcam_settings}"
    os.system(cmd)
    
def preview(camera):
    ##########################################################
    #  Pre:     camera = integer [0,1]
    #  Post:
    #  Example: preview(0)
    ##########################################################
    camera_number=str(camera)
    cmd=f"libcamera-hello -t 0 --camera {camera_number}"
    os.system(cmd)
