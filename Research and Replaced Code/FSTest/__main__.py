# from . import Translation
# from . import Azimuth
from . import AllAxisDrive

debug = bool(int(input("debug mode? 0/1\n")))
AllAxisDrive.start(debug)

# choice = int(input("What would you like to test?\n1. Translation\n2. Azimuth Rotation\n"))
# if(choice == 1):
#     Translation.start()
# elif(choice == 2):
#     Azimuth.start()
    