#include "Component.h"
#include <iostream>

// Create basic class definition responsible for moving the robot
class MicroROV : public Component{
public:
    MicroROV();
    ~MicroROV();

    void Update();
    void AutoUpdate();
    void Stop();
    
protected:

private:
    
};