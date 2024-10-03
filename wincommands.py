import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import cv2 

class Volume():
    def __init__(self):
        # Get the audio device
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        # Get the current volume level
        self.current_volume = self.volume.GetMasterVolumeLevelScalar()

    def increase(self,increase_precent):
        increase_precent /= 100
        new_volume = min(self.current_volume + increase_precent, 1.0)  # Ensure the volume does not exceed 100%
        self.volume.SetMasterVolumeLevelScalar(new_volume, None)
    
    def decrease(self,decrease_percent):
        decrease_percent /= 100
        new_volume = max(self.current_volume - decrease_percent, 0.0)  # Ensure the volume does not below 0
        self.volume.SetMasterVolumeLevelScalar(new_volume, None)
        
class Brightness:
    def __init__(self):
        # Get the current brightness level
        self.current_brightness = sbc.get_brightness(display=0)
    
    def increase(self,level):
        new_brightness = min(self.current_brightness[0] + level, 100)  # Ensure brightness does not exceed 100%
        sbc.set_brightness(new_brightness, display=0)
    
    def decrease(self,level):
        new_brightness = max(self.current_brightness[0] - level, 0)  # Ensure brightness does not below 0
        sbc.set_brightness(new_brightness, display=0)

class Camera:
    def __init__(self):
        # Get the current working directory
        self.current_directory = os.getcwd()
        self.folder_name = 'Photos'
        self.folder_path = os.path.join(self.current_directory, self.folder_name)
        # Create the folder
        os.makedirs(self.folder_path, exist_ok=True)
        self.No_of_pics = len(list(os.listdir(self.folder_path)))

    def WebCamPic(self,timer = 5,n_snaps = 1):
        cam = cv2.VideoCapture(0)
        cv2.namedWindow('Webcam')
        snap_counter = 1
        while True:
            ret, frame = cam.read()
            if not ret or snap_counter > n_snaps:
                break
            frame = cv2.flip(frame,1)
            cv2.imshow('Webcam', frame)
            self.No_of_pics += 1
            img_name = os.path.join(self.folder_path,f"snapshot_{self.No_of_pics}.jpg")
            cv2.imwrite(img_name, frame)
            snap_counter += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.waitKey(timer*10)

obj = Brightness()
obj.decrease(-50)

