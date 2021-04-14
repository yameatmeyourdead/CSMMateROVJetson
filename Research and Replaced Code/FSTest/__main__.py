# from . import Translation
# from . import Azimuth
from . import AllAxisDrive

debug = bool(input("debug mode? 0/1"))
AllAxisDrive.start(debug)

# choice = int(input("What would you like to test?\n1. Translation\n2. Azimuth Rotation\n"))
# if(choice == 1):
#     Translation.start()
# elif(choice == 2):
#     Azimuth.start()
    