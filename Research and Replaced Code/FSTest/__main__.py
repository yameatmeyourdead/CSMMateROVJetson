from . import Translation
from . import Azimuth

choice = input("What would you like to test?\n1. Translation\n2. Azimuth Rotation")
if(choice == 1):
    Translation.start()
elif(choice == 2):
    Azimuth.start()