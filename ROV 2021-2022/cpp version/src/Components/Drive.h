#include "Component.h"
#include <iostream>
#include "../Tools/Vector3D.h"

// Create basic class definition responsible for moving the robot
class Drive : public Component{
public:
    Drive();
    ~Drive();

    void Update();
    void AutoUpdate();
    void Stop();

    void Translate();
    void Rotate();
    
protected:

private:

};