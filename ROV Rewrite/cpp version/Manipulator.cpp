#include "Component.hpp"
#include <iostream>

class Manipulator : public Component {
public:
    Manipulator() {

    }

    ~Manipulator() {

    } // TODO: upon destruction, set all servos to safe duty cycle
    virtual void update() {
        std::cout << "Manipulator Update" << '\n';
    }
};