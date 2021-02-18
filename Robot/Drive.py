from Robot import Component

class Drive(Component):
    print("Hello from Drive.py")

    def Drive():
        print("IM A CONSTRUCTOR")

    def Update(self):
        print("Drive Update")
    
    def autoUpdate(self):
        print("Drive autoUpdate")
    
    def kill(self):
        print("Drive received kill command")
