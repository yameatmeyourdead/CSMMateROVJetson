#include "Component.hpp"
#include <iostream>

class Drive : public Component {
public:
    Drive() {

    }

    // TODO: Upon destruction set all throttles to 0
    ~Drive() {

    } 

    virtual void update() {
       std::cout << "Drive Update" << '\n';
    }
};